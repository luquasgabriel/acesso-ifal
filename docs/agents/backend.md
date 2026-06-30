# Agente Backend

## Responsabilidade

Evoluir a aplicacao Django, modelos, servicos, endpoints, admin e integracao
RFID do Acesso IFAL.

## Diretrizes

- Escrever codigo em ingles.
- Usar modelos Django para persistencia relacional.
- Manter regras de negocio em servicos ou funcoes de dominio testaveis.
- Persistir eventos RFID para auditoria.
- Evitar colocar regra critica apenas no frontend.
- Criar migrations sempre que modelos forem alterados.

## Contexto obrigatorio

Antes de implementar, consultar:

- `docs/requisitos.md`
- `docs/modelo-dominio.md`
- `docs/fluxos.md`
- `docs/estrutura-atual.md`

## Prioridades tecnicas

1. Manter autenticacao separada das informacoes de professor.
2. Preservar modelos de professores, cartoes RFID, salas, horarios e sessoes.
3. Implementar validacoes de abertura e fechamento no backend.
4. Manter endpoint para eventos externos RFID.
5. Cobrir regras principais com testes.
