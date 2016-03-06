#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import sys
import os

pwm = PWM(0x40) # Initialise the PWM device using the default address
pwm.setPWMFreq(600) # Set frequency in Hz

Off = 0  # Min pulse length out of 4096
Lowest = 102  # Lowest visible pulse length out of 4096
Low = 1024  # Low pulse length out of 4096
Mid = 2048  # Middle pulse length out of 4096
High = 3072  # Max pulse length out of 4096
Max = 4096  # Max pulse length out of 4096

Sleep = .0001
Increment = 1

#method_name = str(sys.argv[1])
#task_id = str(sys.argv[2])

class LEDs:
    def PulseLights():
      Step = Lowest
      while (True):
        if Step == Lowest:
          # going up
          while (Step < Max):
            pwm.setPWM(0, 0, Step)
            pwm.setPWM(1, 0, Step)
            Step += Increment
            time.sleep(Sleep)

        else:
          # going down
          while (Step > Lowest):
            pwm.setPWM(0, 0, Step)
            pwm.setPWM(1, 0, Step)
            Step -= Increment
            time.sleep(Sleep)

        return True


    def DimLights():
      Step = Max
      while (Step > Lowest):
        pwm.setPWM(0, 0, Step)
        pwm.setPWM(1, 0, Step)
        Step -= Increment
        time.sleep(Sleep)

      return True


    def LightsOn():
      Step = Lowest
      while (Step < Max):
        pwm.setPWM(0, 0, Step)
        pwm.setPWM(1, 0, Step)
        Step += Increment
        time.sleep(Sleep)

      return True


    def LightsOff():
      Step = Max
      while (Step >= Off):
        pwm.setPWM(0, 0, Step)
        pwm.setPWM(1, 0, Step)
        Step -= Increment
        time.sleep(Sleep)

      return True


#if __name__ == '__main__':
#  eval(method_name)()
#  #uri = ["curl", "-u", "pi:python", "-i", "-H", "\"Content-Type: application/json\"", "-X", "PUT", "-d", '{\"done\":true}', "http://api.fisc.us:8080/pwmtree/api/tasks/" + str(task_id)]
#  #print uri
#  #call(uri)
#  os.system("curl -u pi:python -i -H \"Content-Type: application/json\" -X PUT -d '{\"done\":true}' http://api.fisc.us:8080/pwmtree/api/tasks/" + str(task_id))