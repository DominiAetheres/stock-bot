import json
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Retrieve the Alpha Vantage API key from the environment variables
stockkey = os.getenv("AV_API")

# Load the JSON file containing the search keywords for the app
# Note that the JSON values have been stripped of whitespace for easier parsing
with open(os.path.join(os.getcwd(), "app", "static", "keywords.json"), 'r') as f:
    keyword_data = json.load(f)


def parse_input(user_input):
    """
    This function takes a string input from the user and returns a tuple containing a list of keywords and a list of 
    stock tickers. The input format must be 'keywords: {stock tickers}', with keywords separated by commas and stock 
    tickers separated by commas and enclosed in curly braces. Whitespaces in the input string will be removed.

    Args:
    - user_input (str): a string input from the user

    Returns:
    - tuple: a tuple containing a list of keywords and a list of stock tickers
    """

    # Remove whitespaces from user_input
    user_input = user_input.replace(" ", "")

    # Splitting the user input by ":" to separate the string
    split_input = user_input.split(":")
    if len(split_input) != 2:
        return -1       # input of the wrong format, has to be "keywords: tickers"

    # Get the keyword parts from split_input
    keyword_list = split_input[0].split(",")

    # Split the modified string by comma to create stock_name_list
    stock_name_list = split_input[1].split(",")

    return keyword_list, stock_name_list


def time_selector_constructor(keyword_list, stock_name_list):
    '''
    Constructs the HTTP request params for a time selector modifiable keyword call
    
    Args:
    - keyword_list (list): A list of keywords extracted from user input
    - stock_name_list (list): A list of stock names extracted from user input
    
    Returns:
    - queries (list): A list of HTTP request params
    - selector (str): The time selector keyword
    '''
    queries = []

    # get the time selector
    selector = keyword_list[1]
    
    # check the selected time selector
    if selector == keyword_data["timeSelector"][0]:     # "current"
        # add GLOBAL_QUOTE query for each stock
        for ticker in stock_name_list:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": ticker,
                "apikey": stockkey
            }
            queries.append(params)
    elif selector == keyword_data["timeSelector"][1]:   # "yesterday"
        # add TIME_SERIES_DAILY_ADJUSTED query for each stock
        for ticker in stock_name_list:
            params = {
                "function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": ticker,
                "apikey": stockkey
            }
            queries.append(params)
            
    # return the list of HTTP request params and the selected time selector
    return queries, selector


def range_selector_constructor(keyword_list, stock_name_list):
    """
    Constructs the HTTP request params for a range selector modifiable keyword call.
    
    Args:
        keyword_list: A list of keywords extracted from user input.
        stock_name_list: A list of stock tickers extracted from user input.
        
    Returns:
        A tuple containing a list of constructed HTTP request params and the range selector keyword.
    """
    
    queries = []
    # get the range selector
    selector = keyword_list[1]
    
    # "last week" selector
    if selector == keyword_data["rangeSelector"][0]:    
        for ticker in stock_name_list:
            params = {
                "function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": ticker,
                "apikey": stockkey
            }
            queries.append(params)
    
    # "last month" selector
    elif selector == keyword_data["rangeSelector"][1]:  
        for ticker in stock_name_list:
            params = {
                "function": "TIME_SERIES_WEEKLY_ADJUSTED",
                "symbol": ticker,
                "apikey": stockkey
            }
            queries.append(params)
    
    # "last year" selector
    elif selector == keyword_data["rangeSelector"][2]:  
        for ticker in stock_name_list:
            params = {
                "function": "TIME_SERIES_MONTHLY_ADJUSTED",
                "symbol": ticker,
                "apikey": stockkey
            }
            queries.append(params)
    
    return queries, selector

    
def request_constructor(keyword_list, stock_name_list):
    """
    Constructs HTTP request parameters based on the given keyword and stock ticker lists.

    Args:
        keyword_list (list): List of keywords passed by the user.
        stock_name_list (list): List of stock ticker symbols passed by the user.

    Returns:
        tuple: A tuple containing the constructed queries, query type, and selector.
            - queries (list): A list of dictionaries containing the HTTP request parameters.
            - query_type (int): An integer representing the type of query made.
                - 1: "keywords" query.
                - 2: "timeSelector" query.
                - 3: "rangeSelector" query.
            - selector (str): A string representing the time/range modifier for the query type.

    Raises:
        int: An integer error code indicating the type of error that occurred:
            - -1: Invalid keywords mixed into call.
            - -2: Incorrect argument count.
            - -3: Call contained no keywords.
    """

    # array containing queries for each stock ticker
    queries = []

    # Check if the user request is "overview" to construct the overview request
    overview = keyword_list[0] == "overview"
    if keyword_list[0] in keyword_data["keywords"] or overview:
        if not overview:
            # Ensure all keywords are valid
            for keyword in keyword_list:
                if keyword not in keyword_data["keywords"]:
                    # -1 error means invalid keywords mixed into call
                    return -1
    # Construct the requests for "keywords" calls
        for ticker in stock_name_list:
            params = {
                "function": "OVERVIEW",
                "symbol": ticker,
                "apikey": stockkey
            }
            queries.append(params)
        query_type = 1          # "keywords" query will be 1

        # constructing a true/false matrix for all the options
        option_matrix = []
        for keyword in keyword_data["keywords"]:
            if keyword in keyword_list or overview:
                option_matrix.append(1)
            else:
                option_matrix.append(0)

        return queries, query_type, option_matrix

    # constructs requests for "modifiableKeywords calls"
    elif keyword_list[0] in keyword_data["modifiableKeywords"]:
        if len(keyword_list) != 2:
            # -2 error means argument count not correct !=2
            return -2
        if(keyword_list[1] in keyword_data["timeSelector"]):
            # constructs HTTP request parameters for "timeSelector" call
            queries, selector = time_selector_constructor(keyword_list, stock_name_list)
            query_type = 2      # time selector query will be type 2
        elif(keyword_list[1] in keyword_data["rangeSelector"]):
            # constructs HTTP request parameters for "rangeSelector" call
            queries, selector = range_selector_constructor(keyword_list, stock_name_list)
            query_type = 3      # range selector query will be type 3
        else:
            # the subsequent arguements were not valid
            return -1
        return queries, query_type, selector

    # if call contained no keywords 
    else:
        return -3

    


"""## Testing - python3 app/parsing.py
string = "price, last week : {APPL,TSLA}"
a, b = parse_input(string)
query = request_constructor(a, b)
print(a, b)
print(query)"""