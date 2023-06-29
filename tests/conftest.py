from app.forms import Login, Registration  
from app import app
import pytest

@pytest.fixture(scope='module')
def login_form():
    """
    Pytest fixture that yields a Login form object that can be used for testing.

    This fixture uses the Flask test client to make a POST request to the '/login'
    route, which initializes a Login form object. The form object is then yielded
    so that it can be used in tests.

    Yields:
        Login: A Login form object.
    """
    with app.test_client() as client:
        with client.post('/login'):
            login_form = Login()
        yield login_form


@pytest.fixture(scope='module')
def registration_form():
    """
    Pytest fixture that yields a Registration form object that can be used for testing.

    This fixture uses the Flask test client to make a POST request to the '/register'
    route, which initializes a Registration form object. The form object is then yielded
    so that it can be used in tests.

    Yields:
        Registration: A Registration form object.
    """
    with app.test_client() as client:
        with client.post('/register'):
            registration_form = Registration()
        yield registration_form


@pytest.fixture(scope='module')
def test_client():
    """
    Pytest fixture that yields a test client that can be used for testing.

    This fixture creates a test client using the Flask application configured for
    testing. It then establishes an application context and yields the test client
    so that it can be used in tests.

    Yields:
        FlaskClient: A test client for the Flask application configured for testing.
    """
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client
