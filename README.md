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

## Raspberry Pi

A ponte RFID fica em `rasp_server/server.py`. Ela le UIDs pela entrada padrao e
envia eventos ao backend:

```bash
BACKEND_URL=http://127.0.0.1:8000/api/rfid/events/ \
ROOM_CODE=LAB-01 \
DEVICE_ID=rasp-lab-01 \
API_TOKEN= \
python rasp_server/server.py
```

A documentacao principal do projeto esta em [docs/README.md](docs/README.md).
