
import json
from flask import Flask, request, Response, jsonify 
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
    switch = request.args['switch']
    pin = gSwitches[str(switch)]['Gpio']
    result = getLedStatus(pin)
    return  jsonify({'State': result }), 200

@app.route('/commutator/switch', methods = ['POST'])
def update_Switch():
    global gSwitches
    data = json.loads(request.data)
    switch = data['Switch']
    state = data['State']
    pin = gSwitches[str(switch)]['Gpio']
    setLedStatus(pin, state)
    return state, 200

@app.route('/commutator/switches', methods = ['GET'])
def get_Switches():
    global gSwitches
    activeSwitches = []
    keys = gSwitches.keys()
    for key in keys:
        pin = gSwitches[key]["Gpio"]
        state = getLedStatus(pin)
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
    print(jsonStr)
    return  jsonStr, 200

@app.route('/commutator/mapping', methods = ['POST'])
def update_Mapping():
    global gSwitches    
    list = json.loads(request.data)["ActiveSwitches"]
    gSwitches = {}       
    for item in list:
        pin = item["Gpio"]
        switch = item["Switch"]
        state = "off"
        if (validateGPIO(pin)): 
            initPin(pin)          
            setLedStatus(pin, state)
            gSwitches[str(switch)] = {'Gpio': pin, 'State': state}
        else:
            return  jsonify({'error': "Invalid GPIO "+str(pin)}), 400
    saveGPIOMapping(gSwitches)
    return "",200
