from app import app
from app.parsing import parse_input, request_constructor
from app.api_calls import api_call, format_response
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


def test_login_form(login_form):
    """
    Test the login form object and its validators.

    Steps:
    1. Access form fields and validators from the login_form object.
    2. Assert the types and validators of the form fields.

    Args:
        login_form: The login form object to be tested.
    """

    # Step 1: Access form fields and validators
    username_field = login_form.username
    password_field = login_form.password
    remember_me_field = login_form.remember_me
    submit_field = login_form.submit

    # Step 2: Assert types and validators of form fields
    assert isinstance(username_field, StringField)
    assert isinstance(password_field, PasswordField)
    assert isinstance(remember_me_field, BooleanField)
    assert isinstance(submit_field, SubmitField)
    assert isinstance(username_field.validators[0], DataRequired)
    assert isinstance(password_field.validators[0], DataRequired)


def test_registration_form(registration_form):
    """
    Test the registration form object and its validators.

    Steps:
    1. Access form fields and validators from the registration_form object.
    2. Assert the types and validators of the form fields.

    Args:
        registration_form: The registration form object to be tested.
    """

    # Step 1: Access form fields and validators
    username_field = registration_form.username
    email_field = registration_form.email
    password_field = registration_form.password
    password2_field = registration_form.password2
    submit_field = registration_form.submit

    # Step 2: Assert types and validators of form fields
    assert isinstance(username_field, StringField)
    assert isinstance(email_field, StringField)
    assert isinstance(password_field, PasswordField)
    assert isinstance(password2_field, PasswordField)
    assert isinstance(submit_field, SubmitField)
    assert isinstance(username_field.validators[0], DataRequired)
    assert isinstance(email_field.validators[0], DataRequired)
    assert isinstance(email_field.validators[1], Email)
    assert isinstance(password_field.validators[0], DataRequired)
    assert isinstance(password2_field.validators[0], DataRequired)
    assert isinstance(password2_field.validators[1], EqualTo)




def test_index_parsing_and_api_calls_func():
    """
    Test the parsing and request construction for the index endpoint.

    Steps:
    1. Create a user_input with a keyword and a list of stock names.
    2. Parse the user_input to extract the keyword and stock names.
    3. Construct the request query using the parsed data.
    4. Assert that the parsed data and query are as expected.
    """

    # Step 1: Create a user_input
    keyword = "overview"
    stocks = ["APPL", "TSLA"]
    stocks_string = ",".join(stocks)
    user_input = f'{keyword} : {stocks_string}'

    # Step 2: Parse the user_input
    keywords, stock_names = parse_input(user_input)

    # Step 3: Assert the parsed data
    assert keywords[0] == "overview"
    assert stock_names[0] == "APPL"
    assert stock_names[1] == "TSLA"

    # Step 4: Construct the request api_calls
    api_calls = request_constructor(keywords, stock_names)

    # Assert the constructed api_calls
    assert api_calls[0][0]["function"] == "OVERVIEW"
    assert api_calls[0][0]["symbol"] == "APPL"
    assert api_calls[0][0]["apikey"] == "6EZE5Y75Q8PHXWB3"
    assert api_calls[0][1]["function"] == "OVERVIEW"
    assert api_calls[0][1]["symbol"] == "TSLA"
    assert api_calls[0][1]["apikey"] == "6EZE5Y75Q8PHXWB3"
    assert api_calls[1] == 1
    assert api_calls[2] == [1, 1, 1, 1, 1, 1]

    content = ""
    responses = api_call(api_calls[0])

    if type(responses) == list:
        # response data will contain an array of tuples with format (ticker, data type=list)
        response_data = format_response(responses, api_calls[1], api_calls[2])
        
        for response in response_data:
            content += response[0] + "\n"
            for line in response[1]:
                content += line + "\n"
            content += "\n\n"

    # Assert the content
    assert type(content) == str
    assert content is not None


