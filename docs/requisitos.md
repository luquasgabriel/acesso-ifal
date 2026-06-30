# Requisitos do sistema

## Requisitos funcionais

### Usuarios e professores

- O sistema deve manter usuarios autenticaveis.
- O sistema deve permitir associar um usuario a um professor.
- O cadastro de professor deve possuir matricula funcional e status ativo.
- O cadastro de professor deve permitir associar um ou mais cartoes RFID.

### Cartoes RFID

- O sistema deve validar o UID do cartao RFID recebido da Raspberry Pi.
- O UID deve ser normalizado antes da validacao.
- O valor bruto do UID nao deve ser armazenado.
- O sistema deve armazenar hash do UID e apenas um sufixo mascarado para apoio
  operacional.
- Somente um cartao ativo pode usar o mesmo hash.

### Salas

- O sistema deve catalogar salas.
- Cada sala deve possuir um codigo unico usado pela integracao RFID.
- Cada sala pode estar livre, em uso, bloqueada ou em manutencao.

### Horarios de aula

- O sistema deve registrar horarios recorrentes com professor, sala, disciplina,
  turma, dia da semana, horario de inicio e horario de termino.
- O sistema deve considerar tolerancia para abertura antecipada e atraso.
- O sistema deve permitir desativar horarios sem apagar historico.

### Liberacao por RFID

- O backend deve receber eventos RFID por endpoint HTTP.
- O backend deve validar se o cartao pertence a professor ativo.
- O backend deve validar se existe horario ativo para professor, sala e momento
  do evento.
- O backend deve abrir uma sessao quando a sala estiver livre e a regra permitir.
- O backend deve fechar a sessao quando o professor responsavel usar o RFID em
  uma sala com sessao aberta.
- O backend deve negar tentativas invalidas e registrar o motivo.

### Auditoria

- O sistema deve registrar eventos relevantes de acesso.
- Eventos aceitos e negados devem manter data, hora, sala, identificador
  mascarado, payload bruto e motivo de negacao quando houver.

## Requisitos nao funcionais

- O backend deve ser desenvolvido em Django.
- O banco configurado e PostgreSQL.
- O codigo deve ser escrito em ingles.
- A documentacao deve ser escrita em portugues.
- O sistema deve usar timezone configurado para o contexto local do IFAL.
- Validacoes de acesso devem ocorrer no servidor.
- Segredos e configuracoes devem ficar em variaveis de ambiente.

## Fora do escopo imediato

- Controle eletrico direto de fechaduras pelo Django.
- Cadastro manual fora do Django Admin.
- Aplicativo movel.
- Relatorios academicos de frequencia.
