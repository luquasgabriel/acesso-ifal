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
- `RFID_API_TOKEN`

`RFID_API_TOKEN` e opcional. Quando configurada, o endpoint RFID exige header
`Authorization: Bearer <token>`.

## Convencoes de implementacao

- Nomes de modelos devem estar em ingles e no singular, por exemplo `Room` e
  `AccessSession`.
- Apps Django do projeto devem ficar no pacote `apps/`.
- O dominio operacional fica em `apps.access`.
- Regras de negocio de abertura e fechamento devem ficar em servicos ou casos
  de uso, nao diretamente em views ou admin.
- Eventos RFID devem ser persistidos para auditoria antes ou junto da decisao de
  aceite.
- Validacoes criticas devem ocorrer no backend.

## Estrutura interna dos apps

Cada app Django deve ser organizado de forma modular, separando arquivos por
responsabilidade e evitando arquivos grandes com muitas classes ou funcoes.

- Modelos devem ficar em um pacote `models/`, com um modelo principal por
  arquivo.
- Views devem ficar em um pacote `views/`, com uma view ou grupo pequeno de
  views relacionadas por arquivo.
- Regras de negocio e integracoes de dominio devem ficar em `services/`.
- Constantes compartilhadas devem ficar em `constants.py` ou pacote
  `constants/`, quando necessario.

## Testes esperados

Ao implementar o dominio, priorizar testes para:

- professor autorizado abrindo sala no horario correto;
- professor tentando abrir sala fora do horario;
- cartao RFID desconhecido;
- sala bloqueada ou em manutencao;
- fechamento de sala pelo professor responsavel;
- tentativa de fechamento por professor diferente;
- registro de eventos aceitos e negados.
