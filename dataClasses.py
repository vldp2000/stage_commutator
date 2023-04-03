import json
from json import JSONEncoder

#----------------------------------------------------------------

class Switch(object):
  #Switch = 0,  
  #Gpio = 0,
  #State = 'off'

  def __init__(self, switch, port, state):
    self.Switch = switch
    self.Gpio = port
    self.State = state

  @property
  def Switch(self):
    return self.__Switch

  @property
  def Gpio(self):
    return self.__Gpio

  @property
  def State(self):
    return self.__State

  @Switch.setter
  def Switch(self, switch):
    self.__Switch = switch

  @Gpio.setter
  def Gpio(self, port):
    self.__Gpio = port

  @State.setter
  def State(self, state):
    self.__State = state

  def to_Json(self):
    return json.dumps(
      self, 
      default=lambda o: o.__dict__, 
      allow_nan=False, 
      sort_keys=False, 
      indent=4
    )
  
  def dump(self):
    return {
      'Switch': self.Switch,
      'Gpio': self.Gpio,
      'State': self.State
    }
  
  @staticmethod
  def load(dumped_obj):
    return Switch(
      dumped_obj['SwitchList']['Switch'],
      dumped_obj['SwitchList']['Gpio'],
      dumped_obj['SwitchList']['State'])  

#----------------------------------------------------------------
class CustomEncoder(json.JSONEncoder):
  def default(self, o):
    return {'{}'.format(o.__class__.__name__): o.__dict__}
#----------------------------------------------------------------

def beautify_key(str):
    index = str.index('__')
    if index <= 0:
        return str

    return str[index + 2:]


class MyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return {beautify_key(k): v for k, v in vars(o).items()}

#----------------------------------------------------------------
    