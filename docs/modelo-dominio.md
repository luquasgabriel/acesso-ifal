# Modelo de dominio

Este documento descreve as entidades usadas no Acesso IFAL. Os nomes tecnicos
ficam em ingles para orientar a implementacao.

## Entidades principais

### User

Usuario autenticavel do sistema. Existe no app `accounts`.

Campos principais:

- `username`
- `email`
- `first_name`
- `last_name`
- campos padrao do `AbstractUser`

### Teacher

Representa o professor catalogado.

Campos principais:

- `user`
- `employee_number`
- `is_active`

### RfidCard

Representa um cartao RFID associado a um professor.

Campos principais:

- `teacher`
- `rfid_hash`
- `rfid_suffix`
- `is_active`
- `issued_at`
- `revoked_at`

O UID RFID deve ser normalizado antes de gerar o hash. O sistema nao deve
armazenar o UID bruto.

### Room

Representa uma sala fisica.

Campos principais:

- `name`
- `code`
- `location`
- `capacity`
- `status`

### ClassSchedule

Representa uma aula prevista em horario recorrente.

Campos principais:

- `teacher`
- `room`
- `subject`
- `class_group`
- `weekday`
- `starts_at`
- `ends_at`
- `is_active`

### AccessSession

Representa a liberacao real de uma sala para uma aula.

Campos principais:

- `schedule`
- `teacher`
- `room`
- `opened_at`
- `closed_at`
- `status`
- `opened_by_event`
- `closed_by_event`

### AccessEvent

Representa eventos recebidos da integracao RFID.

Campos principais:

- `source`
- `event_type`
- `room`
- `identifier`
- `occurred_at`
- `accepted`
- `denial_reason`
- `raw_payload`

`identifier` deve guardar apenas uma forma mascarada do identificador recebido.

## Relacionamentos principais

- `Teacher` possui um ou mais `RfidCard`.
- `ClassSchedule` relaciona professor, sala e horario.
- `AccessSession` nasce de uma liberacao valida por RFID.
- `AccessEvent` audita cada tentativa de abertura ou fechamento.

## Organizacao em apps

- `apps.accounts`: autenticacao e usuarios.
- `apps.access`: professores, cartoes RFID, salas, horarios, sessoes e eventos.

## Estados

### Room.status

- `available`
- `in_use`
- `locked`
- `maintenance`

### AccessSession.status

- `open`
- `closed`
- `cancelled`

### AccessEvent.event_type

- `rfid_open_attempt`
- `rfid_close_attempt`
