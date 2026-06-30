# Instrucoes para agentes

Este repositorio usa `AGENTS.md` na raiz como ponto de entrada para agentes.

## Leitura obrigatoria

Antes de propor ou implementar mudancas, consulte:

- `docs/README.md`
- `docs/agents/README.md`
- o arquivo especifico do agente em `docs/agents/`, quando aplicavel

## Convencoes do projeto

- Documentacao em portugues.
- Codigo, nomes de classes, funcoes, variaveis, apps Django, migrations e
  identificadores internos em ingles.
- Textos de interface para usuarios finais em portugues.
- Regras de negocio criticas devem ficar no backend.
- Decisoes relevantes devem ser registradas em `docs/`.

## Contexto do sistema

O Acesso IFAL e um sistema Django para controle de abertura e fechamento de
salas com RFID. A integracao fisica RFID roda fora da aplicacao Django, em uma
Raspberry Pi, e deve ser tratada como fonte de eventos enviada ao backend.
