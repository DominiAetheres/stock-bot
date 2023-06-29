import requests
import json
import os

# Open the keyword file in read mode and load its contents into the `keyword_data` variable.
with open(os.path.join(os.getcwd(), "app", "static", "keywords.json"), 'r') as f:
    keyword_data = json.load(f)

"""
Example usage:
            params = [
                {
                    "function": "OVERVIEW",
                    "symbol": ticker,
                    "apikey": stockkey
                },
                ...
            ]

            response = api_call(params)
"""

URL = "https://www.alphavantage.co/query"

def api_call(queries):
    """
    Call the Alpha Vantage API with the specified queries.

    Parameters:
        queries (list): A list of dictionaries containing the API parameters to use for each query.

    Returns:
        Either a list of JSON response objects, or a HTTP status code or -1 if there is an error.
    """
    response = []
    for params in queries:
        # Send a HTTP GET request to the Alpha Vantage API with the specified parameters.
        reply = requests.get(URL, params)

        # Check the HTTP status code to see if the request was successful.
        if reply.status_code != 200:
            # If the request was not successful, return the HTTP status code.
            return reply.status_code
        else:
            # If the request was successful, parse the JSON response and add it to the response list.
            json_response = reply.json()

            if bool(json_response) is False:
                return -1
            response.append(json_response)
    # Return the response list containing the JSON response objects.
    return response


## format_response prepares a plaintext response to the user
## the "query_type" and "selector" variables from request_constructor() is passed to specify response format
## if query is of a non modifiable type, selector will contain a true/false matrix for all the options

def format_response(response, query_type, selector):
    """
    Formats the response received from the API and returns it in a user-friendly format.

    Args:
    response (list or int): The raw response received from the API.
    query_type (int): An integer value specifying the type of query made by the user.
    selector (list or bool): A list or bool value that is used to format the response based on the user's selection.

    Returns:
    response_data (list): A list containing the formatted response data.

    The `query_type` argument is an integer that specifies the type of query made by the user.
    There are three types of queries:
        1. General keyword search for a stock
        2. Real-time data for a stock
        3. Historical data for a stock

    The `selector` argument is a list that contains boolean values for formatting the response based on the user's selection.
    If the query is of a non-modifiable type, `selector` will contain a true/false matrix for all the options.
    """
    if response == int:
        return response
    
    # formatting the response for a standard keyword
    if query_type == 1:
        # response_data contains an array of tuples in the format (ticker, type=list)
        # ticker field is formatted as: Apple Inc. (AAPL)
        # the list contains the raw response data relevent to the user request, wrapped to be returned to user
        response_data = []
        for stock in response:
            ticker = stock["Name"] + " (" + stock["Symbol"] + ")"
            data = []

            if selector[0] == 1:
                data.append(stock["Description"])
            if selector[1] == 1:
                data.append("Dividend yield: "+ stock["DividendYield"])
            if selector[2] == 1:
                data.append("Dividend per share: "+ stock["DividendPerShare"])
            if selector[3] == 1:
                data.append("EPS: "+ stock["EPS"])
            if selector[4] == 1:
                data.append("PE ratio: "+ stock["PERatio"])
            if selector[5] == 1:
                data.append("Profit margin: "+ stock["ProfitMargin"])
            
            response_data.append((ticker, data))
        
        return response_data
    
    # formatting the response for real-time data
    elif query_type == 2:
        response_data = []
        if selector == keyword_data["timeSelector"][0]:     # "current"
            for stock in response:
                stock = stock["Global Quote"]
                ticker = stock["01. symbol"]
                data = []
                
                data.append("Current price: " + stock["05. price"])
                data.append("Open: " + stock["02. open"])
                data.append("High: " + stock["03. high"])
                data.append("Low: " + stock["04. low"])
                data.append("Volume: " + stock["06. volume"])
                
                response_data.append((ticker, data))
        
        elif selector == keyword_data["timeSelector"][1]:   #"yesterday"
            for stock in response:
                ticker = stock["Meta Data"]["2. Symbol"]
                data = []
                stock = stock["Time Series (Daily)"]
                stock = next(iter(stock.values()))
                
                data.append("Open: " + stock["1. open"])
                data.append("Close: " + stock["4. close"])
                data.append("High: " + stock["2. high"])
                data.append("Low: " + stock["3. low"])
                data.append("Volume: " + stock["6. volume"])
                
                response_data.append((ticker, data))
        #print("\n\n", response_data,"\n\n")
        return response_data
    
    # formatting the response for historical data
    elif query_type == 3:
        response_data = []
        if selector == keyword_data["rangeSelector"][0]:    #"lastweek" will do daily from last week
            for stock in response:
                ticker = stock["Meta Data"]["2. Symbol"]
                data = []
                stock = stock["Time Series (Daily)"]
                counter = 0
                
                for day in stock:
                    if counter == 5:
                        break
                    data.append(day)
                    data.append("Open: " + stock[day]["1. open"])
                    data.append("Close: " + stock[day]["4. close"])
                    data.append("High: " + stock[day]["2. high"])
                    data.append("Low: " + stock[day]["3. low"])
                    data.append("Volume: " + stock[day]["6. volume"])
                    counter += 1
                
                response_data.append((ticker, data))
        
        elif selector == keyword_data["rangeSelector"][1]:  #"lastmonth" will do weekly from last month
            for stock in response:
                ticker = stock["Meta Data"]["2. Symbol"]
                data = []
                stock = stock["Weekly Adjusted Time Series"]
                counter = 0
                
                for day in stock:
                    if counter == 4:
                        break
                    data.append(day)
                    data.append("Open: " + stock[day]["1. open"])
                    data.append("Close: " + stock[day]["4. close"])
                    data.append("High: " + stock[day]["2. high"])
                    data.append("Low: " + stock[day]["3. low"])
                    data.append("Volume: " + stock[day]["6. volume"])
                    counter += 1
                
                response_data.append((ticker, data))
                
        elif selector == keyword_data["rangeSelector"][2]:  #"lastyear will do monthly for a year"
            for stock in response:
                ticker = stock["Meta Data"]["2. Symbol"]
                data = []
                stock = stock["Monthly Adjusted Time Series"]
                counter = 0
                
                for day in stock:
                    if counter == 12:
                        break
                    data.append(day)
                    data.append("Open: " + stock[day]["1. open"])
                    data.append("Close: " + stock[day]["4. close"])
                    data.append("High: " + stock[day]["2. high"])
                    data.append("Low: " + stock[day]["3. low"])
                    data.append("Volume: " + stock[day]["6. volume"])
                    counter += 1
                
                response_data.append((ticker, data))
        #print("\n\n", response_data,"\n\n")
        return response_data