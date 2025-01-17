#include <Wire.h>
#include <BH1750.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <ESPAsyncWebSrv.h>

BH1750 lightMeter;
AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);

  // Initialize the I2C bus (BH1750 library doesn't do this automatically)
  Wire.begin();

  lightMeter.begin();

  // Setup Access Point
  WiFi.softAP("ESP32-AP", "password");

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  // Handle root URL request
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    float lux = lightMeter.readLightLevel();
    String luxString = String(lux, 1);

    String html = "<html><body>";
    html += "<h1>Light Sensor Readings</h1>";
    html += "<p>Light Level: " + luxString + " lx</p>";
    html += "</body></html>";

    request->send(200, "text/html", html);
  });

  // Start server
  server.begin();
}

void loop() {
  // No additional code in the loop function
}
