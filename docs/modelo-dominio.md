# Modelo de dominio

Este documento descreve as entidades esperadas para o Acesso IFAL. Os nomes
tecnicos sugeridos estao em ingles para orientar a implementacao.

## Entidades principais

### User

Usuario autenticavel do sistema. Ja existe no app `accounts`.

Campos atuais:

- `username`
- `email`
- `first_name`
- `last_name`
- campos padrao do `AbstractUser`

Evolucao recomendada:

- adicionar ou relacionar um perfil para identificar papeis como `teacher` e `student`;
- manter autenticacao separada das informacoes academicas especificas.

### Student

Representa o aluno catalogado.

Campos sugeridos:

- `user`
- `registration_number`
- `course`
- `is_active`

### Teacher

Representa o professor catalogado.

Campos sugeridos:

- `user`
- `employee_number`
- `is_active`

Os cartoes RFID devem ser associados ao professor por meio de `RfidCard`.

### RfidCard

Representa um cartao RFID associado a um professor.

Campos sugeridos:

- `rfid_id`
- `teacher`
- `is_active`
- `issued_at`
- `revoked_at`

`rfid_id` e o codigo unico lido pelo leitor RFID. Ele deve ser obrigatorio,
normalizado antes de salvar e unico entre cartoes ativos. Exemplos de
normalizacao: remover espacos, remover separadores e padronizar letras
hexadecimais em maiusculo. No sistema podera haver repeticao, dado que o
cartao pode ser repassado. Mas para isso, o anterior deve ter data de
"revoke".

O sistema deve armazenar um hash do ID em vez do valor bruto, 
mantendo apenas um sufixo mascarado para suporte operacional.

### Room

Representa uma sala fisica.

Campos sugeridos:

- `name`
- `code`
- `location`
- `capacity`
- `qr_code_token`
- `status`

### ClassSchedule

Representa uma aula prevista.

Campos sugeridos:

- `teacher`
- `room`
- `subject`
- `starts_at`
- `ends_at`
- `weekday`, se o horario for recorrente;
- `is_active`

### AccessSession

Representa a liberacao real de uma sala para uma aula.

Campos sugeridos:

- `schedule`
- `teacher`
- `room`
- `opened_at`
- `closed_at`
- `status`
- `opened_by_event`
- `closed_by_event`

### AttendanceRecord

Representa a presenca de um aluno em uma sessao de aula.

Campos sugeridos:

- `session`
- `student`
- `checked_in_at`
- `checked_out_at`
- `status`

### AccessEvent

Representa eventos recebidos dos leitores RFID, QR Codes ou outras origens.

Campos sugeridos:

- `source`
- `event_type`
- `room`
- `identifier`
- `occurred_at`
- `accepted`
- `denial_reason`
- `raw_payload`

`identifier` deve guardar o identificador recebido no evento. Para eventos RFID,
esse valor corresponde ao `rfid_id` lido ou ao hash equivalente; para eventos
de QR Code, corresponde ao token do QR Code.

## Relacionamentos principais

- `Teacher` possui um ou mais `RfidCard`.
- `Room` possui um `qr_code_token` ativo.
- `ClassSchedule` relaciona professor, sala e turma.
- `AccessSession` nasce de uma liberacao valida por RFID.
- `AttendanceRecord` pertence a uma `AccessSession` e a um `Student`.
- `AccessEvent` deve permitir auditar o motivo de cada liberacao, bloqueio,
  entrada ou saida.

## Organizacao em apps

A implementacao Django deve manter os apps do projeto dentro do pacote
`apps/`.

- `apps.accounts`: autenticacao, usuarios e evolucao de papeis gerais.
- `apps.access`: regras e registros ligados a salas, cartoes RFID,
  aulas planejadas, sessoes de acesso e eventos de auditoria.
- `apps.attendance`: registros de entrada e saida por QR Code e calculo do
  status de presenca.

Os apps `access` e `attendance` representam os dois apps de dominio previstos
para esta etapa. A existencia dos apps nao significa que todos os modelos e
servicos ja estejam implementados.

## Estados sugeridos

### Room.status

- `available`
- `in_use`
- `locked`
- `maintenance`

### AccessSession.status

- `open`
- `closed`
- `cancelled`

### AttendanceRecord.status

- `present`
- `partial`
- `absent`
- `invalid`

### AccessEvent.event_type

- `rfid_open_attempt`
- `rfid_close_attempt`
- `qr_check_in`
- `qr_check_out`
