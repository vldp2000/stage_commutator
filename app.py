from flask import Flask
from api import api_bp
from dataIO import *
from dataClasses import *

gSwitches = {} #global dictionary of switches

app = Flask(__name__)
app.register_blueprint(api_bp)

gSwitches = readGPIOMapping()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

