# Analise da estrutura atual

## Estado atual do repositorio

O projeto esta em uma base Django com a seguinte estrutura principal:

- `config/`: configuracoes Django, rotas, ASGI e WSGI;
- `apps/accounts/`: app de usuarios e autenticacao;
- `apps/access/`: app previsto para acesso, RFID, salas, sessoes e auditoria;
- `apps/attendance/`: app previsto para presenca e QR Code;
- `theme/`: app de tema com Tailwind e DaisyUI;
- `templates/`: templates globais do projeto;
- `manage.py`: entrada de comandos Django;
- `requirements.txt`: dependencias Python;
- `README.md`: resumo do projeto.

## Pontos adequados aos requisitos

- O projeto ja usa Django, uma escolha adequada para CRUD administrativo,
  autenticacao, permissoes e dashboards.
- O app `accounts` ja define `AUTH_USER_MODEL` customizado, o que facilita
  evoluir perfis de professor e aluno sem depender diretamente do usuario
  padrao do Django.
- O banco configurado e PostgreSQL, adequado para registrar eventos,
  relacionamentos e auditoria.
- O timezone e idioma estao configurados para contexto brasileiro:
  `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Maceio'`.
- O app `theme` ja prepara uma base visual com Tailwind.

## Lacunas em relacao aos requisitos

- Os apps `access` e `attendance` ainda estao sem modelos, servicos e
  endpoints de dominio implementados.
- O modelo `User` ainda nao diferencia professor, aluno e administrador.
- Ainda nao existem entidades para `Student`, `Teacher`, `Room`,
  `ClassSchedule`, `AccessSession`, `AttendanceRecord` e `AccessEvent`.
- Ainda nao existem endpoints ou servicos para receber eventos da integracao
  externa via sockets/RFID.
- Ainda nao existem telas para cadastro de alunos, professores, salas e horarios.
- Ainda nao existe regra de negocio para abrir, fechar ou validar sessoes de
  aula.
- O template base ainda esta com textos padrao de exemplo do Django Tailwind.
- O arquivo `requirements.txt` aparenta estar codificado com bytes nulos
  possivelmente por UTF-16/UTF-16LE. Isso pode atrapalhar instalacoes com
  `pip install -r requirements.txt` se nao for normalizado para UTF-8.

## Estrutura adotada para evolucao

Os apps Django do projeto devem ficar dentro do pacote `apps/`.

- `apps/accounts`: autenticacao, usuarios e papeis gerais;
- `apps/access`: salas, cartoes RFID, aulas planejadas, abertura e fechamento
  de sessoes, eventos externos e auditoria;
- `apps/attendance`: registros de entrada, saida e status de presenca por QR
  Code.

Essa divisao mantem o app `accounts` focado em autenticacao e concentra o
dominio operacional em dois apps: `access` e `attendance`.

## Proxima etapa tecnica recomendada

1. Definir os modelos de dominio em ingles.
2. Criar migrations para as entidades principais.
3. Registrar os modelos no Django Admin.
4. Implementar servicos de negocio para validar abertura, fechamento e presenca.
5. Criar endpoints para eventos RFID e QR Code.
6. Substituir o template base de exemplo por uma interface inicial do sistema.
