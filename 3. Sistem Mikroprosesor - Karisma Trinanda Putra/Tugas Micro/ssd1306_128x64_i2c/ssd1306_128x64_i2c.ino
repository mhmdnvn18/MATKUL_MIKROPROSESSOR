#include <Wire.h>
#include <BH1750.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESPAsyncWebServer.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

BH1750 lightMeter;
float lightIntensity = 0;
AsyncWebServer server(80);

const char* html_page = R"(
<!DOCTYPE html>
<html>
<head>
  <title>ESP32 Light Intensity Monitoring</title>
  <script>
    var ajaxRequest = new XMLHttpRequest();

    function ajaxLoad(ajaxURL) {
      ajaxRequest.open('GET', ajaxURL, true);
      ajaxRequest.onreadystatechange = function() {
        if (ajaxRequest.readyState == 4 && ajaxRequest.status == 200) {
          var intensity = ajaxRequest.responseText;
          document.getElementById('lightIntensity').innerHTML = intensity + " lx";
        }
      };
      ajaxRequest.send();
    }

    function updateLightIntensity() {
      ajaxLoad('getLightIntensity');
    }

    setInterval(updateLightIntensity, 3000);
  </script>
</head>
<body>
  <h1>ESP32 Light Intensity Monitoring</h1>
  <div id="lightIntensity">--</div>
</body>
</html>
)";

void updateLightIntensity() {
  float lux = lightMeter.readLightLevel();
  lightIntensity = lux;
}

void handleNotFound(AsyncWebServerRequest *request) {
  if (request->url() == "/getLightIntensity") {
    updateLightIntensity();
    request->send(200, "text/plain", String(lightIntensity));
  } else {
    request->send(404, "text/plain", "Not Found");
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  lightMeter.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    while (1);
  }

  delay(2000);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  display.println("BH1750 Test begin");
  display.display();

  server.onNotFound(handleNotFound);
  server.begin();

  Serial.println("Web server started");
}

void loop() {
  server.handleClient();

  float lux = lightMeter.readLightLevel();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");

  display.clearDisplay();
  display.setCursor(0, 20);
  display.print("Light: ");
  display.print(lux);
  display.println(" lx");
  display.display();

  delay(500);
}
