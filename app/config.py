import os

# Set the `basedir` variable to the absolute path of the directory containing this file.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Base configuration class.

    Attributes:
    -----------
    SECRET_KEY : str
        A secret key used by Flask to secure the app. Retrieved from an environment variable if set, or 'temp' if not.
    SQLALCHEMY_DATABASE_URI : str
        The URI of the database to use. Retrieved from an environment variable if set, or a local SQLite database if not.
    SQLALCHEMY_TRACK_MODIFICATIONS : bool
        Whether to track modifications to objects and emit signals. Set to `False` for better performance.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or "temp"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False