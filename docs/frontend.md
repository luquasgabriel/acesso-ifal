# Front-end

## Objetivo

As telas internas do Acesso IFAL servem para acompanhamento operacional. O
cadastro e edicao de dados acontecem no Django Admin.

## Base visual

- Templates de autenticacao usam `templates/base.html`.
- Telas internas usam `templates/dashboard/base.html`.
- Componentes reutilizaveis ficam em `templates/includes/`.
- Textos da interface devem ficar em portugues.
- Identificadores e nomes de arquivos devem ficar em ingles.
- Usar Tailwind CSS e DaisyUI conforme o tema do projeto.

## Telas mantidas

| Template | Rota | Descricao |
|----------|------|-----------|
| `registration/login.html` | `/accounts/login/` | Login |
| `registration/logged_out.html` | `/accounts/logout/` | Saida |
| `dashboard/home.html` | `/dashboard/` | Painel operacional |
| `dashboard/history.html` | `/dashboard/historico/` | Historico de sessoes |
| `rooms/list.html` | `/dashboard/salas/` | Lista de salas |
| `rooms/status.html` | `/dashboard/salas/status/` | Acesso por sala |
| `people/teacher_list.html` | `/dashboard/professores/` | Lista de professores |
| `schedules/list.html` | `/dashboard/horarios/` | Lista de horarios |
| `access/rfid_list.html` | `/dashboard/acesso/rfid/` | Cartoes RFID |
| `access/event_list.html` | `/dashboard/acesso/eventos/` | Auditoria |

## Navegacao

O menu lateral deve destacar:

- Dashboard;
- Historico;
- Acesso por sala;
- Salas;
- Horarios;
- Professores;
- Cartoes RFID;
- Auditoria.

Links administrativos devem apontar para o Django Admin quando houver necessidade
de criar, editar ou excluir dados.

## Contextos esperados

### Dashboard

- `stats.rooms`
- `stats.rooms_in_use`
- `stats.open_sessions`
- `stats.teachers`
- `classes`
- `recent_sessions`

### Salas

- `rooms`

### Horarios

- `schedules`
- `teachers`
- `rooms`

### Professores

- `teachers`

### Cartoes RFID

- `cards`

### Auditoria

- `events`
- `rooms`
- `page_obj`
