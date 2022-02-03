from flask_app import app
from flask_app.controllers import controller_user, controller_trail, controller_review

if __name__=="__main__":
    app.run(debug=True)