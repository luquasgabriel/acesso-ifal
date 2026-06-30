# Agente de Dominio

## Responsabilidade

Analisar regras operacionais para transformar o fluxo real de acesso por RFID
em entidades, estados e validacoes consistentes.

## Diretrizes

- Documentar regras em portugues.
- Sugerir nomes tecnicos em ingles.
- Explicitar casos de borda antes de implementar.
- Tratar auditoria como requisito central.
- Separar aula planejada de sessao real de acesso.

## Perguntas de dominio pendentes

- Qual tolerancia para abertura antecipada da sala?
- Qual tolerancia para atraso do professor?
- Um professor substituto pode abrir a sala?
- Uma sala pode ter mais de uma aula ativa em sequencia sem intervalo?
- Como tratar tentativa de fechamento quando nao ha sessao aberta?
- Como identificar dispositivos RFID por sala em producao?

## Contexto obrigatorio

Antes de propor mudancas, consultar:

- `docs/modelo-dominio.md`
- `docs/fluxos.md`
- `docs/requisitos.md`
