import spidev
import time
import RPi.GPIO as GPIO



class AMT203():
  def __init__(self, bus=0, deviceId=0, cs=8, speed_hz=1000000):   # cs=16
    self.deviceId = deviceId
    self.bus = bus
    self.cs = cs
    self.speed = speed_hz
    GPIO.setmode(GPIO.BCM)
    try:
      print("bus: %s | pin: %s" % (self.bus, self.deviceId))
      self.spi = spidev.SpiDev()
      self.spi.open(self.bus, self.deviceId)
      self.open = True
      self.spi.mode = 0b00
      self.spi.no_cs = True
      print("SPI connected. Device id: ", self.deviceId)
    except:
      self.open = False
      print("Could not connect to SPI device")

    GPIO.setup(self.cs, GPIO.OUT)
    GPIO.output(self.cs, GPIO.HIGH)

  def clean_buffer(self):

    while True:
      first_result = self.spiRW([0x00],self.speed,20)
      #print( first_result )
      if first_result[ 0 ] == 165:
        break;

  def get_position(self):
    #GPIO.output(self.cs, GPIO.LOW)
    attempts = 0
    #print(">>> 1")

    # send rd_pos, expect nop_a5 return value
    first_result = self.spiRW([0x10],self.speed,20)  
    #print( 'first res: ', first_result[ 0 ], ', ', end='' )
    #print(">>> 2")

    # keep sending NOP/0x00 as long as response is nop_a5
    while True:
      first_result = self.spiRW([0x00],self.speed,20)
      attempts = attempts + 1
      if attempts > 100: 
        print(" yuk")
        return -1
      
      if first_result[ 0 ] != 0x10:
        #print( 'got: ', first_result[0], ', ', end ='' )
        break;
    #print(">>> 4")

    attempts = 0
    while True:
      tmp = self.spiRW( [0x00], self.speed, 20 )
      #print( tmp, ',, ', end='' )
      if tmp[ 0 ] == 0x10:
        msb_result = self.spiRW( [0x00], self.speed, 20 )
        break;
      attempts = attempts + 1
      if attempts > 100: 
        #print(" yuk2 ")
        #return -1
        pass

    #print(">>> 5")
    lsb_result = self.spiRW([0x00],self.speed,20)
    #print( hex( msb_result[ 0 ] ), ', ', end ='' )
    #print( hex( lsb_result[ 0 ] ), ', ',  end = '' )
    #print(">>> 6")
    final_result = (msb_result[0]<<8 | lsb_result[0])
    #print(">>> 7")
    self.clean_buffer()
    #print(">>> 8")

    #GPIO.output(self.cs, GPIO.HIGH )
    return final_result

  def set_zero(self):
    self.clean_buffer()
    first_result = self.spiRW([0x70],self.speed,20)
    while first_result[0] != 128:
      first_result = self.spiRW([0x00],self.speed,20)
    print("Zero set was successful and the new position offset is stored in EEPROM")
    self.clean_buffer()
    time.sleep(0.1)

  def get_resolution(self):
    return 4096

  def spiRW(self, values, speed, delay):
    GPIO.output(self.cs, GPIO.LOW)
    #time.sleep(.01)
    msg = self.spi.xfer(values, speed, delay)
    GPIO.output(self.cs, GPIO.HIGH)
    return msg
