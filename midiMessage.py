import pygame
import pygame.midi
import sys
from time import sleep
from apiConfig import *

gExitFlag = False
gMidiDevice = MIDI_OUTPUT_DEVICE  

#----------------------------------------------------------------

def printDebug(message):
  global gMode
  if gMode == 'Debug':
    print(message)

#Main Module 
pygame.midi.init()

# print(str(sys.argv))
if len(sys.argv) > 1: 
  if str(sys.argv[1]).upper() == 'DEBUG':
    gMode = 'Debug'

#Show the list of available midi devices
printDebug(pygame.midi.get_count())
printDebug( pygame.midi.get_default_output_id())
printDebug( pygame.midi.get_device_info(0))
if gMode == 'Debug':
  for id in range(pygame.midi.get_count()):
    printDebug( "Id=%d Device=%s" % (id,pygame.midi.get_device_info(id)) )

portOk = False
midiOutput = None

while not portOk:
  try:
    printDebug(f"Trying to initialize MIDI device {pygame.midi.get_device_info(gMidiDevice)}....")
    midiOutput = pygame.midi.Output(gMidiDevice)
    sleep(0.04)
    portOk = True
  except:
    printDebug("MIDI device not ready....")
    pygame.midi.quit()
    pygame.midi.init()
    sleep(2)

printDebug("Everything ready now...")


while not gExitFlag:
  try:
    printDebug("Semding MIDI  note_on(100,50,1)")
    midiOutput.note_on(100,50,1)
    sleep(3)
  except:
    printDebug("Error sending note!")

#---Close application

del midiOutput
pygame.midi.quit()
