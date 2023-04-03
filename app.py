
import json
import flask
import pprint
from flask import Flask, request, Response, jsonify 
#from flask_api import status
from dataClasses import *
from handleGPIO import *
from dataClasses import *
from dataIO import *

gSwitches = {} #global dictionary of switches

app = Flask(__name__)

gSwitches = readGPIOMapping()
initSwitches(gSwitches)

@app.route('/commutator/switch', methods = ['GET'])
def get_Switch():
    global gSwitches
    switch = request.args.get('switch')
    pin = gSwitches[switch]
    result = getLedStatus(pin)
    return  jsonify({'State': result }), 200

@app.route('/commutator/switch', methods = ['POST'])
def update_Switch():
    data = json.loads(request.data)
    pin = data.Switch
    state = data.State
    setLedStatus(pin, state)
    return state, 200

@app.route('/commutator/switches', methods = ['GET'])
def get_Switches():
    global gSwitches
    pprint.pprint(gSwitches)
    activeSwitches = []
    keys = gSwitches.keys()
    for key in keys:
        pprint.pprint(key)
        pin = gSwitches[key]["Gpio"]
        pprint.pprint(pin)
        state = getLedStatus(pin)
        pprint.pprint(state)
        gSwitches[key]["State"] = state
        activeSwitches.append( Switch(key, pin, state))
    jsonStr = json.dumps(
        activeSwitches,
        indent = 1, 
        #sort_keys=True, 
        skipkeys = True,
        allow_nan = False,
        cls = MyJsonEncoder,
        separators = (',', ': '), 
        ensure_ascii = False 
    )       
    print("-------------------")
    print(jsonStr)
    return  jsonStr, 200

@app.route('/commutator/mapping', methods = ['POST'])
def update_Mapping():
    global gSwitches
    switches = json.loads(request.data)
    gSwitches = {}       
    for item in switches:
        if (validateGPIO(item.Gpio)):           
            setLedStatus(item.Gpio, "off")
            gSwitches[item]["Gpio"] = item.Gpio
            gSwitches[item]["State"] = "off"           
        else:
            return  jsonify({'error': "Invalid GPIO "+item.Gpio}), 400
    saveGPIOMapping(gSwitches)
    return "",200

        
