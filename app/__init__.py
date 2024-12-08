from flask import Flask

app = Flask(__name__)

app.secret_key = 'AlexHome2010'

from app import routes