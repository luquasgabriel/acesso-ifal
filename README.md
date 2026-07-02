# Acesso IFAL

Sistema Django para gerenciamento de professores, cartoes RFID, salas,
horarios de aula e registros de abertura e fechamento de salas.

## Como rodar localmente

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

3. Configure um arquivo `.env` na raiz do projeto de acordo com o `.env.example`

4. Aplique as migracoes e crie um usuario administrador:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Inicie o servidor:

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` e entre com o usuario criado.

## ESP32

A ponte RFID fica em `esp_server/server.py`. Ela sobe um servidor WebSocket
para receber leituras do leitor/ESP32 e encaminha cada evento ao backend Django,
que valida o cartao, a sala e o horario no banco:

```bash
BACKEND_URL=http://127.0.0.1:8000/api/rfid/events/ \
ROOM_CODE=LAB-01 \
DEVICE_ID=rasp-lab-01 \
API_TOKEN= \
RFID_WS_HOST=0.0.0.0 \
RFID_WS_PORT=8080 \
python esp_server/server.py
```

O cliente WebSocket pode enviar JSON com `tipo: "RFID_LIDO"` e `uid`. A resposta
usa `tipo: "STATUS_ACESSO"`, `autorizado`, `acao`, `comando` e o motivo de
negacao quando houver.

A documentacao principal do projeto esta em [docs/README.md](docs/README.md).
