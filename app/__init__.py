from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Create a new Flask application
app = Flask(__name__)

# Load configuration settings from Config object
app.config.from_object(Config)

# Create a new SQLAlchemy object and bind it to the Flask app
db = SQLAlchemy(app)

# Create a new Migrate object to handle database migrations for the Flask app
migrate = Migrate(app, db)

# Create a new LoginManager object to handle user authentication for the Flask app
login = LoginManager(app)


from app import routes, models, parsing, api_calls, parsing