# Guia de desenvolvimento

## Padrao de idioma

- Documentacao: portugues.
- Codigo Python, JavaScript, CSS customizado, nomes de arquivos de apps e
  identificadores internos: ingles.
- Interface do usuario: portugues.
- Commits e pull requests: preferencialmente portugues, exceto nomes tecnicos.

## Stack atual

- Python
- Django 5.2
- PostgreSQL
- Django Tailwind
- Tailwind CSS
- DaisyUI

## Configuracao

O projeto usa `python-decouple`, portanto configuracoes sensiveis devem ficar em
variaveis de ambiente ou em arquivo `.env` local nao versionado.

Variaveis esperadas pelo `config/settings.py`:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `NPM_BIN_PATH`

## Convencoes de implementacao

- Nomes de modelos devem estar em ingles e no singular, por exemplo `Room` e
  `AccessSession`.
- Apps Django do projeto devem ficar no pacote `apps/`.
- O dominio operacional deve ser dividido em dois apps principais:
  `apps.access` para acesso, RFID, salas, sessoes e auditoria; e
  `apps.attendance` para presenca e QR Code.
- Regras de negocio de abertura, fechamento e presenca devem ficar em servicos
  ou casos de uso, nao diretamente em views ou admin.
- Eventos de RFID e QR Code devem ser persistidos para auditoria antes ou junto
  da decisao de aceite.
- Validacoes criticas devem ocorrer no backend.
- Tokens de QR Code devem ser opacos e nao devem expor IDs sequenciais.

## Testes esperados

Ao implementar o dominio, priorizar testes para:

- professor autorizado abrindo sala no horario correto;
- professor tentando abrir sala fora do horario;
- cartao RFID desconhecido;
- aluno registrando entrada em sessao aberta;
- aluno tentando registrar presenca sem sessao ativa;
- fechamento de sala pelo professor responsavel;
- tentativa de fechamento por professor diferente;
- calculo de status de presenca.
