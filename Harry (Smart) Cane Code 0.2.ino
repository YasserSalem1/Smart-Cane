#include <SoftwareSerial.h>   // Header file of software serial port (Lidar Library)
#include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library
SoftwareSerial Serial1(2,3);  // Define software serial port name as Serial1 and define pin2 as RX and pin3 as TX
PulseSensorPlayground pulseSensor;  // Creates a pulseSensor object
#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math
#define HEADER 0x59           // Frame header of lidar's data package
#define motor_speed 200       // Motors fixed speed from 0 to 255
#define obst_dist 30          // The distance where an obstacle is detected in cm
#define enA 9    // Controls motor's speed
#define in1 8    // Controls motor's direction 1
#define in2 7    // Controls motor's direction 2
#define vibr 5   // Vibration motor
#define PulseWire A0       // Pulse sensor signal pin
#define p_threshold 550    // Determine which Signal to "count as a beat" and which to ignore
#define state 12           // Determine whether the board is on or off

void setup()
{
    Serial.begin(9600); //set bit rate of serial port connecting Arduino with computer
    Serial1.begin(115200); //set bit rate of serial port connecting LiDAR with Arduino
    
    // Set all the motor control pins to outputs
    pinMode(enA, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
   
    pinMode(vibr,OUTPUT);   // Setting vibrator as an output

    // Configuring the PulseSensor object by assigning our variables to it
    pulseSensor.analogInput(PulseWire);   
    pulseSensor.setThreshold(p_threshold);
    
}

int lidar()
{
      int uart[9];   // Array that stores data measured by LiDAR
      int dist;      // Stores distance in cm measured by LiDAR
      int check;     // Verifies the received data as per protocol
   // int strength;  // How accurate does the LiDAR thinks its readings are
   // float temp;    // Stores temp in celcuis measured by LiDAR
      if (Serial1.available()) {                // Check if serial port has data input

        if (Serial1.read() == HEADER){          // Assess data package frame header 0x59 
            uart[0] = HEADER;
            
            if (Serial1.read() == HEADER) {   
                uart[1] = HEADER;
        
                for (int i = 2; i < 9; i++) {   // Store data in array
                uart[i] = Serial1.read();
                }
                
                check = uart[0] + uart[1] + uart[2] + uart[3] + uart[4] + uart[5] + uart[6] + uart[7];   // Calculate the check variable
                
                if (uart[8] == (check & 0xff)) {    // Verify the received data as per protocol using the calculated check variable 
                    dist = uart[2] + uart[3] * 256;         // Calculate the distance value
                    // strength = uart[4] + uart[5] * 256;  // Calculate signal strength value
                    // temp = uart[6] + uart[7] * 256;      // Calculate chip temprature
                    // temp = temp / 8 - 256;               // Changing temprature value from 0-255 to celcuis
                    Serial.print("dist: ");
                    Serial.print(dist);
                    Serial.println(" cm");
                 /* Serial.print("strength = ");
                    Serial.print(strength); //output signal strength value
                    Serial.print("\tTemprature = ");
                    Serial.print(temprature);
                    Serial.println("'"); //output chip temperature of Lidar
                 */
                }

            }

        } 

     } 
    return dist;    // Returns the distance
}

void dirt1()   // This function will run the motors in a direction at a fixed speed
{
    // Set speed to 200 out of possible range 0-255
    analogWrite(enA, 200);
    
    // Turn on motor
    Serial.println("Direction 1");
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
}

void dirt2()  // This function will run the motors in a direction at a fixed speed
{
    // Set speed to 200 out of possible range 0-255
    analogWrite(enA, 200);
    
    // Turn on motor
    Serial.println("Direction 2");
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
}

void vibr_l()  // A function the signals the vibrator motor to vibrate at low intervals
{
  digitalWrite(vibr, HIGH); 
  delay(500);  
  digitalWrite(vibr, LOW);    
  delay(250);
  digitalWrite(vibr, HIGH); 
  delay(500);
  digitalWrite(vibr, LOW);
  return;
}

void vibr_lm() // A function the signals the vibrator motor to vibrate at meduim-low intervals
{
  digitalWrite(vibr, HIGH); 
  delay(500);  
  digitalWrite(vibr, LOW);    
  delay(250);
  digitalWrite(vibr, HIGH); 
  delay(750);
  digitalWrite(vibr, LOW);
  return;
}

void vibr_m() // A function the signals the vibrator motor to vibrate at meduim intervals
{
  digitalWrite(vibr, HIGH); 
  delay(750);  
  digitalWrite(vibr, LOW);    
  delay(250);
  digitalWrite(vibr, HIGH); 
  delay(750);
  digitalWrite(vibr, LOW);
  return;
}

void vibr_sos() // A function the signals the vibrator motor to vibrate at SOS intervals
{
  digitalWrite(vibr, HIGH); 
  delay(1000);  
  digitalWrite(vibr, LOW);    
  delay(500);
  digitalWrite(vibr, HIGH); 
  delay(1000);
  digitalWrite(vibr, LOW);
  delay(500);
  digitalWrite(vibr, HIGH); 
  delay(1000);
  digitalWrite(vibr, LOW);
  delay(500);
  return;
}

void loop()
{   
    int state_val = digitalRead(state);      // Checks if the switch is on or off
    if (state_val == HIGH){
      int dist = lidar();          // Get the distance using the lidar function
      Serial.print("dist: "); 
      Serial.print(dist);
      Serial.println(" cm");
      while (obst_dist >= dist){   // Checks if an obstacle is detected withtin 30 cm 
        vibr_l();                  // Vibrates at low intervals
        dirt1();                   // Turns the wheel to direction 1
        delay(4500);
        dist = lidar();            // Rechecks the distance
        Serial.print("dist: "); 
        Serial.print(dist);
        Serial.println(" cm");
          if (obst_dist < dist){          // If the obstacle is overcomed
            Serial.println("Stopping");   
            break;                        // Stop turning
          }
          else {                   // If the obstacle is not overcomed
            vibr_lm();             // Vibrates at low intervals
            dirt2();               // Turns the wheel to direction 2
            delay(9000);
            dist = lidar();        // Rechecks the distance
            Serial.print("dist: "); 
            Serial.print(dist);
            Serial.println(" cm");
              if (obst_dist >= dist){  // If the obstacle is not overcomed yet 
                Serial.println("Raise the cane");
                vibr_m();              // Signals the user to raise the cane
              }
              else {                   // If the obstacle is overcomed at last
                Serial.println("Stopping");     
                break;                 // Stop turning
              }
          }
      }
      
      int BPM = pulseSensor.getBeatsPerMinute();      // Calculates the BPM
      Serial.print("BPM: ");
      Serial.println(BPM);                       
      if (BPM > 100 || BPM < 60){                     // If the BPM is greater or less than the normal
        delay(60000);                                 
        BPM = pulseSensor.getBeatsPerMinute();        // Wait a minute and calculate the BPM again
        Serial.print("BPM: ");          
        Serial.println(BPM);                       
        while (BPM > 100 || BPM < 60){                // If the BPM is still greater or less than the normal
          vibr_sos();                                 // Vibrate at SOS intervals
        }
      }
    }
}
