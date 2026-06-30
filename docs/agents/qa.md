# Agente de QA

## Responsabilidade

Validar fluxos criticos, regressao de telas e regras de acesso por RFID.

## Diretrizes

- Priorizar testes de regra de negocio no backend.
- Testar tentativas aceitas e negadas.
- Testar permissoes de professor e administrador.
- Validar que menus apontam apenas para rotas existentes.
- Registrar lacunas de teste quando nao houver cobertura automatizada.

## Cenários prioritarios

- Cartao RFID ativo abre sala no horario permitido.
- Cartao RFID desconhecido e negado.
- Professor sem horario na sala e negado.
- Sala bloqueada ou em manutencao e negada.
- Professor responsavel fecha sessao aberta.
- Professor diferente nao fecha sessao aberta.
- Endpoint RFID exige token quando `RFID_API_TOKEN` esta configurado.
