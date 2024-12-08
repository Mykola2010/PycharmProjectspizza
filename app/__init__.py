from flask import Flask

app = Flask(__name__)

app.secret_key = 'AlexHome2010'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from app import routes