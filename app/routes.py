from app import app
from app import db
from flask import render_template, flash, redirect, session, request, jsonify
from app.forms import *
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Message
from app.parsing import parse_input, request_constructor
from app.api_calls import *
from sqlalchemy import text

## used for debugging purposes
from pprint import pprint


@app.route('/')
def StockBot():
    '''
    Renders the index page.
    '''
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Route to handle the home page. If the HTTP method is POST, then it processes user input
    and returns the relevant data. If the HTTP method is GET, it renders the index.html template.
    """
    if request.method == "POST":
        data = request.get_json()
        content = data['message']

        # Here we set a default message for not authenticated users
        not_auth_msg = ""
        if not current_user.is_authenticated:
            not_auth_msg = "User not authenticated, your messages will not be saved from this point."

        if(current_user.is_authenticated):
            # if user is authenticated, add message to database and associate it with the user
            message = Message(content=content)
            message.setUser()
            message.setVariableFields(current_user.id)
            pprint(vars(message))

            db.session.add(message)
            db.session.commit()

        ## TODO: return the message, this is where we analyse the message
        success = False     # tracks if message is successfully parsed or contains user input error
        parsed_content = parse_input(content)
        print(parsed_content)

        if type(parsed_content) == tuple:
            # if parsed content is valid, generate API calls based on input and make requests
            api_calls = request_constructor(parsed_content[0], parsed_content[1])

            if api_calls == -1:
                content = "INFO: There were invalid keywords in the input."
            elif api_calls == -2:
                content = "INFO: Keyword count is not correct."
            elif api_calls == -3:
                content = "INFO: Your call must contain keywords! Please check your input."
            else:
                # if API calls are successful, format the response data and return to user
                responses = api_call(api_calls[0])
                if type(responses) == list:
                    response_data = format_response(responses, api_calls[1], api_calls[2])
                    content = ""
                    for response in response_data:
                        content += response[0] + "\n"
                        for line in response[1]:
                            content += line + "\n"
                        content += "\n\n"
                        success = True
                elif responses == -1:
                    content = "INFO: A stock ticker may be misspelt, or does not exist."
                else:
                    content = "INFO: There was an issue with the Alpha Vantage API. HTTP code: "+ response
        else:
            content = "INFO: The input format was invalid."

        if current_user.is_authenticated:
            # if user is authenticated, add response message to database and associate it with the user
            message = Message(content=content)
            message.setResponse()
            message.setVariableFields(current_user.id)
            pprint(vars(message))

            # add message to database
            db.session.add(message)
            db.session.commit()

        post_response = {
            "success": success,
            "content": content,
            "not_auth_msg": not_auth_msg   # add the not_auth_msg to the response
        }

        return jsonify(post_response)
    
    else:
        return render_template("index.html")




@app.route('/history')
@login_required
def history():
    """
    Route to handle the history page. Renders the history.html template.
    Also queries database for userId's old messages and returns them.
    """
    messages_object = db.session.execute(text("SELECT * FROM message WHERE userId==" + str(current_user.id) + " ORDER BY timeStamp DESC;"))
    sent, response, sent_timestamp, response_timestamp = [], [], [], []

    for message in messages_object:
        if message.isUser == True:
            sent.append(message.content)
            sent_timestamp.append(message.timeStamp[:19])
        else:
            response.append(message.content)
            response_timestamp.append(message.timeStamp[:19])

    return render_template("history.html", messages=zip(sent_timestamp, sent, response_timestamp, response))

@app.route('/help')
def help():
    '''
    Renders the help page.
    '''
    return render_template("help.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Renders the login page. If a user is already authenticated, they are redirected to the home page. 
    If the login form is submitted with valid credentials, the user is logged in and redirected to the home page.
    '''
    if current_user.is_authenticated:
        return redirect("/")
    
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  # Get the user from the database based on the submitted username
        if user is None or not user.checkPassword(form.password.data): # If the user doesn't exist or the password is incorrect
            flash("Invalid username or password")
            return redirect("/login")
        else: # If the user exists and the password is correct
            login_user(user)
            return redirect("/")
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Renders the registration page. If a user is already authenticated, they are redirected to the home page. 
    If the registration form is submitted with valid information, a new user is created and redirected to the login page.
    '''
    if current_user.is_authenticated:
        return redirect("/")
    
    form = Registration()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.setPassword(form.password.data)

        # add user to database
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    
    # if form is not submitted and not valid, render the registration page
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    '''
    Logs the user out and redirects them to the home page. If the user was once logged in, their session is cleared.
    '''
    logout_user()
    if session.get("was_once_logged_in"):
        del session["was_once_logged_in"]
    return redirect("/")
