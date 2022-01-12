import time
from machine import Pin
from machine import Timer
from mqtt import MQTTClient

pinout = Pin(4, Pin.OUT)
pinin = Pin(12, Pin.IN, Pin.PULL_UP)  #D5
c = MQTTClient("seba", "192.168.0.10",user="seba", password="masty", port=1883)

if (pinin.value()==0):
  pinout.value(1)
else:
  pinout.value(0)
print(pinout.value())

timer = Timer(0)

def przelacz(timer):
  #print('jestem w timer')
  if (pinin.value()==0):
    pinout.value(1)
  else:
    pinout.value(0)
  
  
def zwloka():
  #print('przeszłem do zwloki')
  timer.init(period=900000, mode=Timer.ONE_SHOT, callback=przelacz)
  while True:
    time.sleep_ms(500)
    if (pinin.value()!=pinout.value()):
      timer.deinit()
      return
  
def petla():
  #print('jestem w petli')
  while True:
    time.sleep(600)
    if (pinin.value()==1):
      try:
        c.connect()
        c.publish('domoticz/in','{"command": "switchlight", "idx": 38, "switchcmd": "Off"}')
        c.disconnect()
      except:
        pass
    if (pinin.value()==0):
      try:
        c.connect()
        c.publish('domoticz/in','{"command": "switchlight", "idx": 38, "switchcmd": "On"}')
        c.disconnect()
      except:
        pass
    if (pinin.value()==pinout.value()):
      zwloka()
