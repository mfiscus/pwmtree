#!/usr/bin/env python
#Copyright 2013, Peter Cock. All rights reserved.
#Released under the MIT License.
"""Python scipt to generate Roomba IR codes for LIRC.
 
Tested under Python 2.7 and Python 3.3, example usage:

$ python make_roomba_lirc.py > roomba.conf

See also:
http://astrobeano.blogspot.com/2013/10/roomba-620-infrared-signals.html
http://astrobeano.blogspot.com/2013/11/raspberry-pi-ir-blaster-and-roomba-ir.html
"""

def encode(code, interval=1000):
    values = []
    for i in range(8):
        if code & 2**(7-i):
            values.extend([interval*3, interval]) #one
        else:
            values.extend([interval, interval*3]) #zero
    return values

# Power = 0x8A = 1000 1010
# which is 3ms on, 1ms off; 1ms on, 3ms off; ...; 1ms on, 3ms off.
assert encode(0x8A, 1) == [3,1, 1,3, 1,3, 1,3, 3,1, 1,3, 3,1, 1,3]
assert encode(0x8A) == [3000, 1000, 1000, 3000, 1000, 3000, 1000, 3000,
                        3000, 1000, 1000, 3000, 3000, 1000, 1000, 3000]

def format_code(code, interval=1000, repeat=2, pause=16000):
    values = encode(code, interval)
    values[-1] += pause # extend off of last bit into full pause
    values = values*repeat
    values = values[:-1] # remove trailing off
    answer = []
    while values:
        batch = values[:6]
        values = values[6:]
        answer.append(" "*9 + "".join(str(v).rjust(8) for v in batch))
    return "\n".join(answer)

header = """# Automatically generated LIRC Roomba config file

begin remote

  name   iRobot_Roomba
  flags RAW_CODES|CONST_LENGTH
  eps            30
  aeps          100

  ptrail          0
  repeat     0     0
  gap   100000

      begin raw_codes
"""

footer = """
      end raw_codes

end remote
"""

codes = [
    #Roomba Remote:
    (0x81, "Left"),
    (0x82, "Forward"),
    (0x83, "Right"),
    (0x84, "Spot"),
    (0x85, "Dock"), #aka Max
    (0x86, "Small"),
    (0x87, "Medium"),
    (0x88, "Clean"), #aka Large
    (0x89, "Pause"),
    (0x8A, "Power"),
    (0x8B, "ForwardLeft"),
    (0x8C, "ForwardRight"),
    (0x8D, "Stop"),
    #Scheduling remote:
    (0x8E, "SendAll"),
    (0x8F, "SeekDocK"),
    #Virtual wall:
    (0xA2, "VirtualWall"),
]

print(header)
for code, name in codes:
    print("          name %s" % name.lower())
    print(format_code(code))
    print("")
print(footer)
