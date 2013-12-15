//#include <Dhcp.h>
//#include <Dns.h>
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetClient.h>
//#include <EthernetServer.h>
//#include <EthernetUdp.h>

#include <PS2X_lib.h>

PS2X ps2x;

int error = 0; 
byte type = 0;
byte vibrate = 55;

byte mac[] = {0x00, 0xDE, 0xFA, 0xCE, 0xD0, 0x69};
//byte ip[] = {10, 6, 0, 230}; //arduino fixed IP if dhcp fails
//byte gateway[] = {10, 6, 0, 254};
//byte subnet[] = {255, 255, 0, 0};
IPAddress ip(10, 6, 0, 230); //arduino fixed IP if dhcp fails
IPAddress gateway(10, 6, 0, 254);
IPAddress subnet(255, 255, 0, 0);
//IPAddress server(10, 6, 0, 17); //testing connection server
IPAddress server(10, 3, 1, 199); //production connection server
EthernetClient client;
int port = 8080;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  
  
  error = ps2x.config_gamepad(7,5,6,8, true, true);   //setup pins and settings:  
 //GamePad(clock, command, attention, data, Pressures?, Rumble?) check for error
 //Looks like data needds to be on a PWM output
 //Pin Colours and Ports:
 //  Data:    Black:    8
 //  Command: Brown:    5
 //  Attn:    Green:    6
 //  Clk:     Blue:     7
 //  Power:   Yellow:   3v3
 //  Gnd:     Orange:   gnd
 //  Vibe:    Red:      5v0
 
  if(error == 0){
   Serial.println("Found Controller, configured successful");
  }
   
  else if(error == 1)
   Serial.println("No controller found, check wiring, see readme.txt to enable debug. visit www.billporter.info for troubleshooting tips");
   
  else if(error == 2)
   Serial.println("Controller found but not accepting commands. see readme.txt to enable debug. Visit www.billporter.info for troubleshooting tips");
   
  else if(error == 3)
   Serial.println("Controller refusing to enter Pressures mode, may not support it. ");
   
  type = ps2x.readType(); 
     switch(type) {
       case 0:
        Serial.println("Unknown Controller type");
       break;
       case 1:
        Serial.println("DualShock Controller Found");
       break;
       case 2:
         Serial.println("GuitarHero Controller Found");
       break;
     }
     
  // give the ethernet module time to boot up:
  delay(1000);
  
  Serial.println("Connecting to ASS-Bot...");
  if( Ethernet.begin(mac) == 0)
  {
    Serial.println("Failed to configure Ethernet using DHCP");
    Ethernet.begin(mac, ip);
  }
  Serial.println(Ethernet.localIP());
  delay(1000);
  
  //client.connect(server, port);
  
}

//int tmp = 0;

void loop() {
  // put your main code here, to run repeatedly: 
  if(error == 1) //skip loop if no controller found
    return;
    
  ps2x.read_gamepad(false, vibrate);
  
  //Use start button to exit program... reset to start
  //if(ps2x.Button(PSB_START))
  //  return;
    
  // Left analogue stick to control robot movements
  // Right analogue stick to control peripheral movements
  // Using select to switch between peripherals
  
  String controlString = "";
  
  controlString+="Rx=";
  controlString+=ps2x.Analog(PSS_RX);
  controlString+="&Ry=";
  controlString+=ps2x.Analog(PSS_RY);
  controlString+="&Lx=";
  controlString+=ps2x.Analog(PSS_LX);
  controlString+="&Ly=";
  controlString+=ps2x.Analog(PSS_LY);
  controlString+="&BtnX=";
  controlString+=ps2x.Analog(PSAB_BLUE);
  
//  Serial.println(ps2x.Analog(PSS_LY),DEC);
//  Serial.println(ps2x.Analog(PSS_RY),DEC);
//  controlString+="&tempInt=";
//  controlString+=tmp;
  
//  tmp+= 1;
  
  Serial.println(controlString);
  sendData(controlString);
  
  //if(ps2x.Button(PSS_LY))
  //{
  //  Serial.print("Left Analog");
  //  Serial.print(ps2x.Analog(PSS_LY),DEC); //Y-axis
  //  Serial.print(":");
  //  Serial.print(ps2x.Analog(PSS_LX),DEC); //X-axis
  //}
  
  delay(1000);
}

void sendData(String myData)
{
  Serial.print("Preparing to send html data: ");
  Serial.println(myData);
  // if there's a successful connection:
  
  int state = client.connect(server, port);
  //int state = client.connected();
  //Serial.println(state);
  
  if ( state ) {
    Serial.println("connecting...");
    // send the HTTP PUT request:
    client.println("POST /control HTTP/1.1");
    client.println("Host: 10.6.0.4");
    client.println("From: RemoteControl");
    client.println("User-Agent: Arduino/1.5");
    client.println("Connection: close");  
    client.println("Content-Type: application/x-www-form-urlencoded"); 
    client.print("Content-Length: ");
    client.println(myData.length());

    // last pieces of the HTTP PUT request:
    client.println();
    // here's the actual content of the PUT request:
    client.println(myData);
    client.println();
    
    Serial.println("Message sent...");
    
    client.stop();
  } 
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");

    //if no connection, restart the connection
    Serial.println("Restarting connection.");
      // give the ethernet module time to boot up:

    client.stop();
    //client.flush();
    //client.connect(server, port);
    delay(1000);
  }
  
}
