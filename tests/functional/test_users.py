from app import app

def test_home_page(test_client):
    """
    Test the home page '/' of a Flask application.

    Steps:
    1. Send a GET request to the '/' page.
    2. Check that the response status code is 200.
    3. Check that the response data contains the expected content.

    Args:
        test_client: The test client object for the Flask application.
    """

    # Step 1: Send a GET request to the '/' page
    response = test_client.get('/')

    # Step 2: Check the response status code
    assert response.status_code == 200

    # Step 3: Check the response data for expected content
    assert b"StockBot" in response.data


def test_home_page_post(test_client):
    """
    Test the POST request to the home page '/' of a Flask application.

    Steps:
    1. Send a POST request to the '/' page.
    2. Check that the response status code is 400.
    3. Check that the response data does not contain the expected content.

    Args:
        test_client: The test client object for the Flask application.
    """

    # Step 1: Send a POST request to the '/' page
    response = test_client.post('/')

    # Step 2: Check the response status code
    assert response.status_code == 400

    # Step 3: Check the response data for expected content
    assert b"StockBot" not in response.data


def test_help_page():
    """
    Test the help page '/help' of a Flask application.

    Steps:
    1. Send a GET request to the '/help' page.
    2. Check that the response status code is 200.
    3. Check that the response data contains the expected content.

    """

    # Step 1: Send a GET request to the '/help' page
    with app.test_client() as client:
        response = client.get('/help')

        # Step 2: Check the response status code
        assert response.status_code == 200

        # Step 3: Check the response data for expected content
        assert b'Getting Started' in response.data
        assert b'Using the StockBot' in response.data
        assert b'Viewing Your Conversation History' in response.data

'''
def test_get_chat_page():
    """
    Test the chat page '/chat' of a Flask application.

    Steps:
    1. Send a GET request to the '/chat' page.
    2. Check that the response status code is 200.
    3. Check that the response data contains the expected content.

    """

    # Step 1: Send a GET request to the '/chat' page
    with app.test_client() as client:
        response = client.get('/chat')

        # Step 2: Check the response status code
        assert response.status_code == 200

        # Step 3: Check the response data for expected content
        assert b'<form class="input-form" method="POST" action="/chat">' in response.data
        assert b'Type your message here...' in response.data
        assert b'<button type="submit">Send</button>' in response.data


def test_post_chat_page():
    """
    Test the chat page '/chat' of a Flask application when a user submits a valid chat message.

    Steps:
    1. Send a POST request to the '/chat' page with a valid chat message.
    2. Check that the response status code is 200.
    3. Check that the response data contains the expected content, including the updated chat history.

    """

    # Step 1: Send a POST request to the '/chat' page with a valid chat message
    with app.test_client() as client:
        chat_message = 'Hello'
        response = client.post('/chat', data={'text_input': chat_message})

        # Step 2: Check the response status code
        assert response.status_code == 200

        # Step 3: Check the response data for expected content, including the updated chat history
        assert b'<div class="chat-window">' in response.data
        assert f'<p>{chat_message}</p>'.encode() in response.data

'''