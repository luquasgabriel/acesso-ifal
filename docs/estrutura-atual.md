# Analise da estrutura atual

## Estado atual do repositorio

O projeto esta em uma base Django com a seguinte estrutura principal:

- `config/`: configuracoes Django, rotas, ASGI e WSGI;
- `apps/accounts/`: app de usuarios e autenticacao;
- `apps/access/`: dominio de professores, cartoes RFID, salas, horarios,
  sessoes e auditoria;
- `theme/`: app de tema com Tailwind e DaisyUI;
- `templates/`: templates globais do projeto;
- `rasp_server/`: ponte para envio de eventos RFID a partir da Raspberry Pi;
- `manage.py`: entrada de comandos Django;
- `requirements.txt`: dependencias Python;
- `README.md`: resumo do projeto.

## Pontos implementados

- O projeto usa Django e o admin nativo para cadastro dos dados principais.
- O app `accounts` define `AUTH_USER_MODEL` customizado.
- O app `access` concentra o dominio operacional.
- O backend possui endpoint para receber eventos RFID.
- O servico de RFID normaliza e valida UID, sala, professor, horario e sessao.
- Eventos aceitos e negados sao persistidos em `AccessEvent`.
- O timezone e idioma estao configurados para contexto brasileiro:
  `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Maceio'`.

## Estrutura adotada

Os apps Django do projeto ficam dentro do pacote `apps/`.

- `apps.accounts`: autenticacao e usuarios;
- `apps.access`: regras e dados de acesso por RFID.

O cadastro de professores, cartoes RFID, salas e horarios ocorre pelo Django
Admin. As telas internas sao somente leitura e servem para acompanhamento
operacional.

## Pontos de atencao

- A integracao fisica RFID depende da configuracao da Raspberry Pi.
- O endpoint RFID pode exigir `RFID_API_TOKEN` quando a variavel estiver
  configurada.
- As tolerancias de abertura estao definidas no servico de RFID e podem ser
  promovidas para configuracao persistida quando necessario.
