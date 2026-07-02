# Visao geral do projeto

## Objetivo

O Acesso IFAL organiza os dados necessarios para controlar o uso de salas por
RFID. O sistema mantem professores, cartoes RFID, salas e horarios de aula, e
registra eventos de abertura e fechamento recebidos de dispositivos externos.

## Contexto operacional

1. O professor aproxima o cartao RFID do leitor da sala.
2. O ESP32 recebe a leitura e envia o evento ao backend Django.
3. O backend valida o cartao, o professor, a sala e o horario.
4. Se a validacao permitir, a sala e marcada como em uso e uma sessao e aberta.
5. Ao final da aula, o professor aproxima o cartao novamente.
6. O backend valida a sessao aberta, fecha a sessao e libera a sala.
7. Todas as tentativas aceitas e negadas ficam registradas para auditoria.

## Integracao com RFID

A aplicacao Django nao controla diretamente o leitor RFID. A pasta
`esp_server/` contem uma ponte WebSocket para comunicação com o ESP32. Ela
recebe leituras RFID do leitor/ESP32, envia eventos HTTP ao backend e
responde ao cliente WebSocket com a decisao de acesso.

Eventos enviados ao backend devem conter:

- UID do cartao RFID;
- codigo da sala;
- identificador do dispositivo, quando disponivel;
- data e hora da leitura;
- metadados tecnicos relevantes.

## Escopo

O sistema deve manter:

- usuarios autenticaveis;
- professores;
- cartoes RFID vinculados a professores;
- salas;
- horarios de aula;
- sessoes de acesso;
- eventos de auditoria.
