#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

pwm = PWM(0x40) # Initialize PWM device
pwm.setPWMFreq(600) # Set frequency in Hz

Off = 0  # Min pulse length out of 4096
Lowest = 102  # Min pulse length out of 4096
Low = 1024  # Min pulse length out of 4096
Mid = 2048  # Middle pulse length out of 4096
High = 3072  # Max pulse length out of 4096
Max = 4096  # Max pulse length out of 4096


Sleep = .0001
Step = Max
Increment = 1

print "going down"
while (Step > Lowest):
  pwm.setPWM(0, 0, Step)
  pwm.setPWM(1, 0, Step)
  Step -= Increment
  time.sleep(Sleep)

