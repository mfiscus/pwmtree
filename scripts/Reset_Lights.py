#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

pwm = PWM(0x40, debug=True)

pwm.softwareReset()

#pwm.setPWMFreq(600)                        # Set frequency in Hz

#pwm.setPWM(0, 0, 0)
#time.sleep(.0001)
#pwm.setPWM(1, 0, 0)
#time.sleep(.0001)

#pwm = PWM(0x40)
