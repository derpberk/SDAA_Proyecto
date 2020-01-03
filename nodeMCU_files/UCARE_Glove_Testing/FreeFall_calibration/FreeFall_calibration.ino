
#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire);

long timer = 0;
float ax,ay,az;
int p = 0;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu6050.begin();
}

void loop() {
  mpu6050.update();

  if(millis() - timer > 100 && p <450){

    ax = mpu6050.getAccX();
    ay = mpu6050.getAccY();
    az = mpu6050.getAccZ();
    
    Serial.println(sqrt(ax*ax+ay*ay+az*az));
    p++;
    timer = millis();
  
  }

}
