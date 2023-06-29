from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import select, text
from datetime import datetime

class User(UserMixin, db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.

    Methods:
        __repr__(): Returns a string representation of the user object.
        setPassword(password): Sets the password hash for the user using the provided plaintext password.
        checkPassword(password): Checks if the provided plaintext password matches the user's stored password hash.

    Inherits from:
        UserMixin: A mixin class from Flask-Login that provides default implementations for methods required by the Flask-Login extension.
        db.Model: A base class from SQLAlchemy that provides functionality for interacting with a database model.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def loadUser(id):
    """
    Retrieves a User object from the database using the provided ID.

    Args:
        id (int): The ID of the user to retrieve.

    Returns:
        A User object representing the user with the provided ID, or None if no such user exists.
    """
    return User.query.get(int(id))


class Message(db.Model):      
    # Three primary keys for easy access to messages
    # Message id for a given user increments by 1 each time since there is no interaction between users
    # Every time the user initiates a new conversation, the conversationId increments by 1.    
    # Therefore a unique message can be fetched purely by a primary key of a combined userId, conversationId and id.
    # When loading the page, the user will be promted to choose a conversation or start a new one. 
                     
    id = db.Column(db.Integer, primary_key=True)
    conversationId = db.Column(db.Integer, primary_key=True)
    parentId = db.Column(db.String(36))
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    timeStamp = db.Column(db.DateTime)
    content = db.Column(db.Text)
    isUser = db.Column(db.Boolean)
    
    def setVariableFields(self, userId):
        '''
        Sets the fields which may change for each userId: id, parentId, timeStamp.
        '''
        self.userId = userId
    
        # Get the maximum id and conversationId for the user
        currentIdObject = db.session.execute(text("SELECT MAX(id) FROM Message WHERE userId==" + str(userId) + ";"))
        currentId = currentIdObject.fetchone()[0]
        
        currentConvIdObject = db.session.execute(text("SELECT MAX(conversationId) FROM Message WHERE userId==" + str(userId) + ";"))
        currentConvId = currentConvIdObject.fetchone()[0]

        # Set the parentId, id, timeStamp, and conversationId fields
        if currentId is not None:
            self.parentId = currentId
            self.id = currentId + 1
        else:
            self.parentId = 0
            self.id = 1
        if currentConvId is not None:       ## logic might need fixing depending on handling of conversations
            self.conversationId = currentConvId
        else:
            self.conversationId = 1
        self.timeStamp = datetime.now()

    def __repr__(self):
        """
        Returns a string representation of the message object.

        Returns:
            A string representation of the message object.
        """
        return '<Message {}>'.format(self.content)
        
    def setUser(self):
        """
        Sets the isUser attribute of the message to True.
        """
        self.isUser = True
    
    def setResponse(self):
        """
        Sets the isUser attribute of the message to False.
        """
        self.isUser = False