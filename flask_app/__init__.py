from flask import Flask
app = Flask(__name__)
app.secret_key = "take a hike"

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

DATABASE = 'hike-app'

