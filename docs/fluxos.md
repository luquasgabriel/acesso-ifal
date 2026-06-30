# Fluxos principais

## Abertura da sala pelo professor

1. O leitor RFID detecta o cartao do professor.
2. A Raspberry Pi envia o evento ao backend.
3. O backend localiza o cartao RFID ativo pelo hash do UID normalizado.
4. O backend identifica o professor associado.
5. O backend verifica se existe horario ativo para o professor na sala e no
   momento permitido.
6. Se a regra for valida, o backend cria uma `AccessSession` aberta.
7. A sala passa para o estado `in_use`.
8. O evento e registrado como aceito.

Caso a regra falhe, o evento deve ser registrado como negado com o motivo.

## Fechamento da sala pelo professor

1. O professor aproxima o cartao RFID do leitor da sala.
2. A Raspberry Pi envia o evento ao backend.
3. O backend identifica a `AccessSession` aberta para a sala.
4. O backend valida se o cartao pertence ao professor responsavel pela sessao.
5. O backend grava `closed_at`.
6. A sala volta para o estado `available`.
7. O evento e registrado como fechamento aceito.

## Tentativas negadas

Tentativas negadas devem gerar `AccessEvent` para auditoria. Exemplos:

- UID RFID ausente ou invalido;
- cartao RFID desconhecido ou inativo;
- sala nao encontrada;
- professor sem aula naquele horario;
- sala bloqueada ou em manutencao;
- sala ja em uso sem sessao compativel;
- professor diferente tentando fechar a sessao.
