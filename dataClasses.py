import json

#----------------------------------------------------------------

class Switch(object):
  Number = 0,  
  GPIO = 0,
  State = 'off'
  def __init__(self, num, port, st):
    self.Number = num
    self.GPIO = port
    self.State = st

  def getNumber(self):
      return self.Number

  def getGPIO(self):
      return self.GPIO

  def getstate(self):
      return self.State

#----------------------------------------------------------------

class CustomEncoder(json.JSONEncoder):
  def default(self, o):
    return {'{}'.format(o.__class__.__name__): o.__dict__}

#----------------------------------------------------------------