# StockBot
This web app was completed for the main project of CITS3403 at UWA.

#### Contributors:
```
Ethan Dai
Jae Won Jo
Kate Kalugina
Harvey Walker
```
StockBot provides users an appealing, powerful, and simple interface into the American stock market. Instead of performing multiple searches or navigating through a website to obtain basic data that may be needed to inform investments, StockBot's syntax allows multiple lookups with a single search for a variety of different data points. This is achieved through our use of the Alpha Vantage API to wrap multiple endpoints into a single response for the user.

## Getting Started...
StockBot allows for the user to interact with it using a very simple query language, which is also explained in the help page of the website. The fundamental idea is:
```
keyword 1, keyword 2 : ticker 1, ticker 2
```
Whitespace does not matter. An example query could be:
```
overview:aapl,tsla,ibm,amzn
```

## Accessing History
Only logged in users can access their previous chat history with StockBot. To register an account, simply click register in the top navigation bar. To log in, click log in and provide your details. 

Once logged in, the history button should appear in the navigation bar. History will display all previous conversations with StockBot and the server time at which they were sent. A simple search function is provided on the right hand side which instantly matches your search with whats currently in your history.

## StockBot's Architecture
StockBot comprises of a frontend running on JavaScript aided by the Jinja2 Python library, a Flask backend, and an SQLite database. 

Some aspects of the frontend are directly managed by Flask using Jinja2 such as the log in, register and history pages. This allows for the dynamic generation of HTML elements before returning the webpage to the user and automatic return of data to Flask without any frontend involvement. The messages aspect of StockBot uses the HTTP protocol to communicate with the backend as this allows for the dynamic generation of HTML elements while the website is in use. 

The Flask backend is responsible for liaising between the frontend and the SQLite database and Alpha Vantage API. The database contains two tables: "user" and "message". The users are all assigned an id, which is a primary key in user in addition to being a foreign key and part of a primary key tuple in message. Messages are simply stored with an ascending message id for each user.

## Launching the Application
** Note, you MUST have an Alpha Vantage api key to run this app. The api key should be stored in ```./app/.env``` as
as ```AV_API=yourkey```.

Make sure to install all dependencies on your python interpreter using
```
pip install -r requirements.txt
```
Then set your environment variable and run the app
```
set FLASK_APP=run.py
```
```
flask run
```
The unit tests are mentioned at the bottom.

## Keeping the main branch up to date and working
Please only merge or commit directly to main after checking with everyone - main should hold a working build.

Please generate a new requirements.txt everytime new modules are added to your venv. Please delete any deprecated modules. You can use this command:
```
pip freeze > requirements.txt
```

## How to get this working?
After creating your own branch, make sure to create a Python venv to run the flask app.

To create in the current directory:
``` 
python -m venv ./venv
```

Make sure to run the activate.bat (on Windows cmd) or equivalent to activate the venv.

Then to install all dependencies:
```
pip install -r requirements.txt
```

To run a development server on your local machine, you must first set the FLASK_APP environment variable:
```
set FLASK_APP=run.py
```

Then, the development server can be run by:
```
flask run
```

## Simple queries for the database
To check that your code works properly the the database, we can use sqlite3 to query it.

We can normally navigate to the directory of the app.db, then we can open it using sqlite3:
```
.open app.db
```

The schema can be checked:
```
.schema
```

A refresher to SQL queries, the following simple ones are provided:
```
SELECT * FROM user;
```
```
SELECT * FROM message;
```

## How to run test cases
To run the tests, navigate to the top-level folder of the Flask project and run pytest through the Python interpreter:
```
python -m pytest
```

To see more details on the tests that were run:
```
python -m pytest -v
```

If you only want to run a specific type of test:
- python -m pytest tests/unit/
- python -m pytest tests/functional/

## How to run selenium tests
To validate the behaviour of our bot, selenium tests were used. They cover great amount of user functions. To run the tests, run the development server. Open the Python interpreter and run:

```
python ./tests/selenium_test.py
```

Tests can be run on Chrome, Firefox or Egde. Go to selenium_test.py and change the browser:
browser = "chrome" # to run on Chrome
browser = "firefox" # to run on Firefox
browser = "edge" #to run on Edge
