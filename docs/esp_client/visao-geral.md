# Sistema de Controle de Acesso às salas do IFAL - IoT com ESP32

Este documento detalha o funcionamento da implementação do cliente do sistema. Foi utilizado um ESP32, com comunicação com o servidor acontecendo via WebSocket para validação de credenciais RFID. O sistema integra hardware de autenticação, feedback visual/sonoro e simulação do controle de uma fechadura física.

---

## Funcionalidades
- **Autenticação RFID:** Leitura de cartões/tags via módulo MFRC522.
- **Conectividade:** Comunicação em tempo real com servidor via WebSockets.
- **Feedback:**
  - Display LCD I2C para mensagens de status.
  - Led RGB para sinalização de acesso (permitido/negado).
  - Módulo DFPlayer Mini para avisos sonoros.
- **Controle Físico:** Abertura de trava via Servo Motor e fechamento manual por botão.

---

## Pré-requisitos para Reprodução
Certifique-se de ter instalado na Arduino IDE as seguintes bibliotecas:
- `MFRC522`
- `WebSockets` (por Markus Sattler)
- `ArduinoJson`
- `ESP32Servo`
- `hd44780`
- `DFRobotDFPlayerMini`

---

## Configuração
Antes de compilar, edite as constantes no início do código:

```cpp
const char* ssid = "SUA_REDE_WIFI";
const char* password = "SUA_SENHA";
String serverIp = "IP_DO_SEU_SERVIDOR";
int serverPort = 8080;