from flask import Flask
from config import Config
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
# mysql://username:password@server/db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Excalibur789!@database-1.cj6y4kwxksyv.us-east-1.rds.amazonaws.com/sys'

# this is the session timeout
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)
db = SQLAlchemy(app)

# start up login
login = LoginManager(app)

from app import routes, models


if __name__ == '__main__':
    app.run(debug=True)

