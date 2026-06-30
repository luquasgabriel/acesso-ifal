# Agente Frontend

## Responsabilidade

Construir telas administrativas e operacionais para usuarios do Acesso IFAL.

## Diretrizes

- Textos da interface em **portugues**.
- Identificadores, nomes de blocos e arquivos de template em **ingles**.
- Seguir a paleta de cores do projeto: verde `#67C180`, verde claro `#D7F5E1`,
  cinza escuro `#232323`, cinza medio `#71717A`, cinza claro `#969696`.
- Usar daisyUI v5 com Tailwind CSS v4 para componentes de interface.
- Nao criar telas de CRUD: dados sao inseridos via Django Admin.
- Templates de listagem sao somente leitura, sem botoes de criar/editar/excluir.
- Usar heranca de templates: `base.html` para autenticacao,
  `dashboard/base.html` para telas internas com sidebar + header.
- Componentes reutilizaveis em `templates/includes/`.
- Responsividade: usar classes responsivas (`sm:`, `md:`, `lg:`) e
  `overflow-x-auto` em tabelas.

## Telas esperadas

| Template | Tipo | Descricao |
|----------|------|-----------|
| `registration/login.html` | Autenticacao | Login |
| `registration/logged_out.html` | Autenticacao | Confirmacao de logout |
| `registration/password_reset_form.html` | Autenticacao | Solicitar redefinicao |
| `registration/password_reset_done.html` | Autenticacao | Email enviado |
| `registration/password_reset_confirm.html` | Autenticacao | Nova senha |
| `registration/password_reset_complete.html` | Autenticacao | Senha alterada |
| `dashboard/home.html` | Dashboard | Painel operacional |
| `dashboard/history.html` | Dashboard | Historico de sessoes de acesso |
| `rooms/list.html` | Salas | Lista de salas |
| `rooms/status.html` | Salas | Acesso por sala |
| `people/teacher_list.html` | Pessoas | Lista de professores |
| `schedules/list.html` | Horarios | Lista de horarios |
| `access/rfid_list.html` | Acesso | Cartoes RFID |
| `access/event_list.html` | Acesso | Log de auditoria |
| `includes/header.html` | Include | Cabecalho |
| `includes/sidebar.html` | Include | Menu lateral |
| `includes/pagination.html` | Include | Paginacao reutilizavel |
| `includes/messages.html` | Include | Toast de mensagens |

## Contexto obrigatorio

Antes de implementar, consultar:

- `docs/visao-geral.md`
- `docs/requisitos.md`
- `docs/fluxos.md`
