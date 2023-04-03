import json

#----------------------------------------------------------------

class Switch(object):
  Switch = 0,  
  Gpio = 0,
  State = 'off'
  def __init__(self, num, port, st):
    self.Switch = num
    self.Gpio = port
    self.State = st

  def getSwitch(self):
      return self.Switch

  def getGpio(self):
      return self.Gpio

  def getState(self):
      return self.State

#----------------------------------------------------------------

class CustomEncoder(json.JSONEncoder):
  def default(self, o):
    return {'{}'.format(o.__class__.__name__): o.__dict__}

#----------------------------------------------------------------