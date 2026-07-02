#include <SPI.h> // não precisa instalar manualmente
#include <MFRC522.h>
#include <WiFi.h> // não precisa instalar manualmente
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h>
#include <Preferences.h> // não precisa instalar manualmente
#include <Wire.h> // não precisa instalar manualmente
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>
#include "DFRobotDFPlayerMini.h"

const char* ssid = "S23 Ultra de José"; // modificar rede
const char* password = "neto12344"; // modificar senha

#define SS_PIN 5
#define RST_PIN 2
#define LED_RED 14
#define LED_GREEN 12
#define LED_BLUE 13
#define SERVO_PIN 32
#define BOTAO_PIN 25

Servo meuServo;
MFRC522 mfrc522(SS_PIN, RST_PIN);
WebSocketsClient webSocket;
hd44780_I2Cexp lcd;
DFRobotDFPlayerMini dfplayer;

bool portaAberta = false;
unsigned long tempoLedVermelho = 0;
String serverIp = "10.154.228.155"; // modificar IP do servidor 
int serverPort = 8080;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);

  lcd.begin(20, 4);
  lcd.backlight();
  lcd.print("Sistema Iniciado");

  Serial2.begin(9600, SERIAL_8N1, 16, 17);
  if (dfplayer.begin(Serial2)) {
    dfplayer.volume(25);
    dfplayer.play(1); 
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  
  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  pinMode(BOTAO_PIN, INPUT_PULLUP);

  meuServo.setPeriodHertz(50);
  meuServo.attach(SERVO_PIN, 500, 2400);
  meuServo.write(0);

  webSocket.begin(serverIp.c_str(), serverPort, "/");
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  if (type == WStype_TEXT) {
    JsonDocument doc;
    deserializeJson(doc, (char*)payload);
    const char* comando = doc["comando"];
    bool autorizado = doc["autorizado"].as<bool>();

    if (autorizado) {
      if (comando != nullptr && strcmp(comando, "ABRIR_PORTA") == 0) {
        if (!portaAberta) {
          meuServo.write(90);
          portaAberta = true;
          digitalWrite(LED_GREEN, HIGH);
          lcd.clear();
          lcd.print("Acesso Autorizado");
          dfplayer.play(2);
        }
      }
    } else {
      digitalWrite(LED_RED, HIGH);
      tempoLedVermelho = millis(); 
      lcd.clear();
      lcd.print("Acesso Negado");
      dfplayer.play(3); 
    }
  }
}

void loop() {
  webSocket.loop();

  if (digitalRead(LED_RED) == HIGH && (millis() - tempoLedVermelho >= 2000)) {
    digitalWrite(LED_RED, LOW);
  }

  if (digitalRead(BOTAO_PIN) == LOW && portaAberta) {
    meuServo.write(0); 
    portaAberta = false;
    digitalWrite(LED_GREEN, LOW);
    delay(500); 
  }

  if (!portaAberta && mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      uid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      uid += String(mfrc522.uid.uidByte[i], HEX);
    }
    
    digitalWrite(LED_BLUE, HIGH);
    
    JsonDocument doc;
    doc["tipo"] = "RFID_LIDO";
    doc["uid"] = uid;
    String output;
    serializeJson(doc, output);
    webSocket.sendTXT(output);
    
    delay(200);
    digitalWrite(LED_BLUE, LOW);
    mfrc522.PICC_HaltA();
  }
}