import pygame
import pygame.midi
import sys
import socket
import struct

from array import *
from time import sleep
from config import *
import dataHelper


#Global Variables
gExitFlag = False
gMidiDevice = MIDI_INPUT_DEVICE  # Input MIDI device
gRaveloxClient = None

#----------------------------------------------------------------

def printDebug(message):
  global gMode
  if gMode == 'Debug':
    print(message)

#----------------------------------------------------------------

def connectRavelox():
  global gRaveloxClient
  try:
    connect_tuple = ( RAVELOX_HOST, RAVELOX_PORT )
    gRaveloxClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gRaveloxClient.connect( connect_tuple )   
    return True
  except:
    # pprint.pprint(sys.exc_info())
    return False

#----------------------------------------------------------------

def sendGenericMidiCommand(msg0, msg1, msg2):
  # global gRaveloxClient

  message = ""
  message = struct.pack("BBB", msg0, msg1, msg2)
  gRaveloxClient.send(message )      
  
  if gMode == 'Debug':
    printDebug("SEND RAVELOX GENERIC MESSAGE %d %d %d" % (msg0, msg1, msg2))

#----------------------------------------------------------------


#----------------------------------------------------------------
def getMidiMsg(midiInput):
  # printDebug("..... LISTEN TO MIDI MSG")
  keepAliveCounter = 0
  checkRaveloxCounter = 0
  gotMsg = 0
  while not(gotMsg):
    sleep(MIDI_RECEIVE_DELAY)
    if midiInput.poll():    
      gotMsg = 1
      inp = midiInput.read(100)
      for midiMsg in inp:
        msg = midiMsg[0]
        msg0 = msg[0]
        msg1 = msg[1]
        msg2 = msg[2]
        sendGenericMidiCommand(msg0, msg1, msg2)

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
        result = dataHelper.unicodetoASCII(str(data))
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
#----------------------------------------------------------------

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
    result = connectRavelox()

    if result:
      midiInput = pygame.midi.Input(gMidiDevice)
      sleep(0.04)
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

#getListOfRaveloxMidiClients()
#sleep(1)

while not gExitFlag:
  getMidiMsg(midiInput)

#---Close application
#gRaveloxClient.close()
gRaveloxClient.shutdown(2)

del midiInput
pygame.midi.quit()
