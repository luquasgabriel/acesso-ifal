import asyncio
import json
import logging
from pathlib import Path

import requests
from decouple import AutoConfig
from requests import RequestException


PROJECT_ROOT = Path(__file__).resolve().parents[1]
config = AutoConfig(search_path=str(PROJECT_ROOT))

BACKEND_URL = config("BACKEND_URL", default="http://127.0.0.1:8000/api/rfid/events/")
ROOM_CODE = config("ROOM_CODE", default="")
DEVICE_ID = config("DEVICE_ID", default="rasp-rfid")
RFID_API_TOKEN = config("RFID_API_TOKEN", default="")
API_TOKEN = config("API_TOKEN", default="") or RFID_API_TOKEN
REQUEST_TIMEOUT = config("REQUEST_TIMEOUT", default=5.0, cast=float)
RFID_WS_HOST = config("RFID_WS_HOST", default="0.0.0.0")
RFID_WS_PORT = config("RFID_WS_PORT", default=8080, cast=int)

RFID_MESSAGE_TYPES = {"RFID_LIDO", "RFID_READ", "RFID_READING"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("rasp_server")


def get_first(data, *keys, default=None):
    for key in keys:
        value = data.get(key)
        if value not in (None, ""):
            return value
    return default


def parse_message(message):
    if isinstance(message, bytes):
        message = message.decode("utf-8")

    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        data = {"tipo": "RFID_LIDO", "uid": message.strip()}

    if not isinstance(data, dict):
        raise ValueError("Mensagem deve ser um objeto JSON ou um UID em texto.")

    return data


def build_backend_payload(data):
    message_type = str(get_first(data, "tipo", "type", default="RFID_LIDO")).upper()
    if message_type not in RFID_MESSAGE_TYPES:
        raise ValueError(f"Tipo de mensagem nao suportado: {message_type}.")

    uid = get_first(data, "rfid_uid", "uid", "rfid_id", "card_uid")
    room_code = get_first(data, "room_code", "room", "sala", default=ROOM_CODE)
    device_id = get_first(data, "device_id", "deviceId", "reader_id", default=DEVICE_ID)
    occurred_at = get_first(data, "occurred_at", "timestamp", "read_at")

    if not uid:
        raise ValueError("UID RFID nao informado.")
    if not room_code:
        raise ValueError("room_code ausente e ROOM_CODE nao configurado no ambiente.")

    payload = {
        "rfid_uid": str(uid),
        "room_code": str(room_code),
        "device_id": str(device_id),
        "source": "rasp_server.websocket",
        "message_type": message_type,
    }
    if occurred_at:
        payload["occurred_at"] = str(occurred_at)

    return payload


def send_to_backend(payload):
    headers = {"Content-Type": "application/json"}
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"

    response = requests.post(
        BACKEND_URL,
        json=payload,
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )

    try:
        body = response.json()
    except ValueError:
        body = {
            "accepted": False,
            "error": "Backend retornou uma resposta que nao e JSON.",
        }

    return response.status_code, body


def build_websocket_response(status_code, result):
    accepted = bool(result.get("accepted"))
    event_type = result.get("event_type")
    command = None
    action = "negar"

    if accepted and event_type == "rfid_open_attempt":
        command = "ABRIR_PORTA"
        action = "abrir"
    elif accepted and event_type == "rfid_close_attempt":
        command = "FECHAR_PORTA"
        action = "fechar"

    return {
        "tipo": "STATUS_ACESSO",
        "autorizado": accepted,
        "accepted": accepted,
        "acao": action,
        "comando": command,
        "event_id": result.get("event_id"),
        "event_type": event_type,
        "session_id": result.get("session_id"),
        "session_status": result.get("session_status"),
        "room_status": result.get("room_status"),
        "motivo": result.get("denial_reason") or result.get("error") or "",
        "denial_reason": result.get("denial_reason", ""),
        "backend_status": status_code,
    }


async def process_rfid_message(message):
    data = parse_message(message)
    payload = build_backend_payload(data)

    try:
        status_code, result = await asyncio.to_thread(send_to_backend, payload)
    except RequestException as exc:
        logger.exception("Falha ao enviar evento RFID ao backend.")
        return {
            "tipo": "STATUS_ACESSO",
            "autorizado": False,
            "accepted": False,
            "acao": "negar",
            "comando": None,
            "motivo": "Backend indisponivel.",
            "error": str(exc),
        }

    return build_websocket_response(status_code, result)


async def handler(websocket):
    peer = getattr(websocket, "remote_address", "cliente")
    logger.info("Cliente WebSocket conectado: %s", peer)

    try:
        async for message in websocket:
            try:
                response = await process_rfid_message(message)
            except ValueError as exc:
                response = {
                    "tipo": "STATUS_ACESSO",
                    "autorizado": False,
                    "accepted": False,
                    "acao": "negar",
                    "comando": None,
                    "motivo": str(exc),
                    "denial_reason": str(exc),
                }

            await websocket.send(json.dumps(response))
    finally:
        logger.info("Cliente WebSocket desconectado: %s", peer)


async def main():
    try:
        import websockets
    except ImportError as exc:
        raise SystemExit(
            "Dependencia ausente: instale websockets com `pip install -r requirements.txt`."
        ) from exc

    logger.info(
        "Servidor RFID WebSocket em ws://%s:%s apontando para %s",
        RFID_WS_HOST,
        RFID_WS_PORT,
        BACKEND_URL,
    )
    async with websockets.serve(handler, RFID_WS_HOST, RFID_WS_PORT):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Servidor RFID WebSocket encerrado.")
