#include <ESP8266WiFi.h>
#include <Adafruit_NeoPixel.h>
#define PIN        2 
#define NUMPIXELS 64 // Popular NeoPixel ring size


Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
char* ssid = "";
char* password =  "";
 
uint16_t port = 8090;
char * host = "192.168.1.7";
WiFiClient client;
IPAddress     TKDServer(192,168,1,7);
uint8_t rgb_vals[192];

void setup()
{

  Serial.begin(9600);
  //WiFi.setSleepMode(WIFI_NONE_SLEEP);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
  while (!client.connect(TKDServer, port)) {

      Serial.println("Connection to host failed");

      delay(1000);
  }
  Serial.println("Connected to server successful!");
  pixels.begin();
  pixels.clear(); 
}
 
void loop(){
    client.print("!");
    if(client.available()){
      pixels.clear(); 
      client.read(rgb_vals, NUMPIXELS * 3); //so this works

      for(int i = 0; i < NUMPIXELS * 3; i = i + 3){
        pixels.setPixelColor(i/3, pixels.Color(rgb_vals[i], rgb_vals[i + 1], rgb_vals[i + 2]));
      }
      
      pixels.show();
    }
    //Serial.println("Disconnecting...");
    //client.stop();
    delay(1);
}
