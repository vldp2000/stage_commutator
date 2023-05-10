import pygame
import pygame.midi
import sys
import socket
import struct

from array import *
from time import sleep
from raveloxConfig import *
from dataHelper import *


#Global Variables
gExitFlag = False
gMidiDevice = MIDI_INPUT_DEVICE  # Input MIDI device
gRaveloxClient = None
gMode = 'Live'
gDelayCounter = 0
#----------------------------------------------------------------

def printDebug(message):
  global gMode
  if gMode == 'Debug':
    print(message)

#----------------------------------------------------------------
def connectToRaveloxMidi():
  global gRaveloxClient
  try:
    local_port = RAVELOX_PORT
    local_host = RAVELOX_HOST
    family = socket.AF_INET
    connect_tuple = ( local_host, local_port )
    gRaveloxClient = socket.socket( family, socket.SOCK_DGRAM )
    gRaveloxClient.connect( connect_tuple )
    sleep(0.5)
    return True
  except:
    print("Error. Can not connect to RaveloxMidi")
    return False

#----------------------------------------------------------------

def sendGenericMidiCommand(msg):
  global gDelayCounter
  message = struct.pack("BBB", int(msg[0]), int(msg[1]), int(msg[2]))
  gRaveloxClient.send(message)
  gDelayCounter = 0
  if gMode == 'Debug':
    printDebug(f"SEND RAVELOX GENERIC MESSAGE {message}")

#----------------------------------------------------------------


#----------------------------------------------------------------
def getMidiMsg(midiInput):
  gotMsg = 0
  while not(gotMsg):
    if midiInput.poll():    
      gotMsg = 1
      inp = midiInput.read(10)
      for midiMsg in inp:
        try:
          msg = midiMsg[0]
          if (msg[0] != 248 and msg[1] != 0 and msg[2] != 0):
            printDebug(f"Message received : {midiMsg}")         
            sendGenericMidiCommand(msg)
        except:
          printDebug(f"Error. incoming message {midiMsg} can not be processed")

#----------------------------------------------------------------

def getListOfRaveloxMidiClients():
  global gRaveloxClient
  # Request status
  bytes = struct.pack( '4s', b'LIST' )

  #print(bytes)
  data = ''
  result = ''
  gRaveloxClient.sendall( bytes )

  x = 0
  while True:
    try:
      data,addr = gRaveloxClient.recvfrom(8192)
      if data:
        result = unicodetoASCII(str(data))
        break
    except:
      pass
    sleep(MIN_DELAY)
    if (x > 5):
      break
    x = x + 1   
##  if result.find("Vlad-iPad") > -1:
      ##
##  if result.find("Vlad's MacBook Pro") > -1:
      ## 

#################################################################
#Main Module 
#pygame.init()
pygame.midi.init()

# print(str(sys.argv))
if len(sys.argv) > 1: 
  if str(sys.argv[1]).upper() == 'DEBUG':
    gMode = 'Debug'

#Show the list of available midi devices
printDebug(pygame.midi.get_count())
if gMode == 'Debug':
  for id in range(pygame.midi.get_count()):
    printDebug( "Id=%d Device=%s" % (id,pygame.midi.get_device_info(id)) )


portOk = False
midiInput = None

while not portOk:
  try:
    result = connectToRaveloxMidi()

    if result:
      printDebug("Connected to raveloxmidi...")
      printDebug(f"Trying to initialize MIDI device {pygame.midi.get_device_info(gMidiDevice)}....")
      midiInput = pygame.midi.Input(gMidiDevice)
      sleep(1)
      portOk = True
    else:
      printDebug("waiting for raveloxmidi...")
      sleep(1)

  except:
    printDebug("MIDI device not ready....")
    pygame.midi.quit()
    pygame.midi.init()
    sleep(2)

printDebug("Everything ready now...")

# There is a method available to extract the list of all the RaveloxMidi subscribers
#getListOfRaveloxMidiClients()

######################
# Main Loop
######################
gDelayCounter = 0
while not gExitFlag:
  getMidiMsg(midiInput)
  gDelayCounter += 1
  if (gDelayCounter > 1000):
    sleep(MIDI_RECEIVE_DELAY)
    gDelayCounter = 1000

####################
#Close application
gRaveloxClient.shutdown(2)
del midiInput
pygame.midi.quit()
