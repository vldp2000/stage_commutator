from flask import Flask, request, abort
from api import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

