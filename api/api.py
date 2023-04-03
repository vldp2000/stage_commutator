import json
from flask import Flask, request, jsonify, responce, status
from . import api_bp
from handleGPIO import *
from dataClasses import *
from dataIO import *

@api_bp.route('/commutator/switch', method = 'GET')
def get_Switch():
    global gSwitches
    switch = request.args.get('switch')
    pin = gSwitches[switch]
    result = getLedStatus(pin)
    return result, status.HTTP_200_OK 

@api_bp.route('/commutator/switch', method = 'POST')
def update_Switch():
    data = json.loads(request.data)
    pin = data.Switch
    state = data.State
    setLedStatus(pin, state)
    return state, status.HTTP_200_OK  

@api_bp.route('/commutator/switches', method = 'GET')
def get_Switches():
    global gSwitches
    activeSwitches = []
    keys = gSwitches.keys()
    for key in keys:
        pin = gSwitches[key]["Gpio"]
        state = getLedStatus(pin)
        gSwitches[key]["State"] = state
        activeSwitches.append( Switch(key, pin, state))
    return  jsonify(activeSwitches), status.HTTP_200_OK

@api_bp.route('/commutator/mapping', method = 'POST')
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
            return  jsonify({'error': "Invalid GPIO "+item.Gpio}), status.HTTP_400_BAD_REQUEST
    saveGPIOMapping(gSwitches)
    return status.HTTP_200_OK



