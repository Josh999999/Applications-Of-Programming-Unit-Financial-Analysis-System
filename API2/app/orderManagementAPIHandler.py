import os
import requests
import json
from datetime import datetime

ORDER_MANAGEMENT_API_KEY=os.getenv('ORDER_MANAGEMENT_API_KEY')


"""Gets the orders ordered over a given date range"""
def get_orders(start_date: str, end_date: str) -> json:

    # Make sure dates are given
    if (not start_date or not end_date):
        # Possibly to many orders to make API return without date constraints
        return "No date parameters endtered", 500
    
    # Query the order API with the date constraints for orders
    url = 'http://ordermanagementsystem:5002//api/orders/date' # Docker containers running internally reference each order by image names


    # Curate request parameters and headers

    # Temp keep api key here statically and get from .env file when run in docker
    # Give the API key for the order management system
    headers = {
        'Authorization': f"Bearer {ORDER_MANAGEMENT_API_KEY}",
    }
    
    """
    # Don't need following code for the moment - Solution for comparing dates in sql inside the order management system without converting them to integers
    # Don't need following code for the moment - Order management system also now handles date formating
    
    # Code fix - change date format from dd/mm/yyyy to yyyymmdd for more reliable query results - can convert to integer in SQL by not inserting quotes:
    
    # Convert to datetime object
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")

    # Convert to desired format - OrderManagementSystem dates are kept as "%Y-%m-%d" for comparison operations in SQLLite - remove "-" and interpret as integer
    start_date = start_date.strftime("%Y%m%d") # When there are no quotes in a query these dates will be interpreted as integers
    end_date = end_date.strftime("%Y%m%d")
    """
    
    params = {
        "start_date": start_date,
        "end_date": end_date
    }
    
    try:
        # Send request
        response = requests.get(url=url, headers=headers, params=params)

        # Format request response
        if response.status_code == 200:
            orders = response.json()

            # Return data in JSON format
            return orders, 200
        else:

            # Return error if request failed (status code is not 200)
            return f"Failed to retrieve data: {response.status_code}", response.status_code
    except:
        return f"Failed to establish connection", 403


"""Gets the quantity of items ordered over a given date range"""
def get_order_items(start_date: str, end_date: str) -> json:

    # Make sure dates are given
    if (not start_date or not end_date):
        # Possibly to many orders to make API return without date constraints
        return "No date parameters endtered", 500
    
    # Query the order API with the date constraints for orders
    url = 'http://ordermanagementsystem:5002//api/orders/items/quantity/date' # Docker containers running internally reference each order by image names


    # Curate request parameters and headers

    # Temp keep api key here statically and get from .env file when run in docker
    # Give the API key for the order management system
    headers = {
        'Authorization': f"Bearer {ORDER_MANAGEMENT_API_KEY}",
    }

    """
    # Don't need following code for the moment - Solution for comparing dates in sql inside the order management system without converting them to integers
    # Don't need following code for the moment - Order management system also now handles date formating

    # Code fix - change date format from dd/mm/yyyy to yyyymmdd for more reliable query results - can convert to integer in SQL by not inserting quotes:
    
    # Convert to datetime object
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")

    # Convert to desired format - OrderManagementSystem dates are kept as "%Y-%m-%d" for comparison operations in SQLLite - remove "-" and interpret as integer
    start_date = start_date.strftime("%Y%m%d") # When there are no quotes in a query these dates will be interpreted as integers
    end_date = end_date.strftime("%Y%m%d")
    """

    params = {
        "start_date": start_date,
        "end_date": end_date
    }
    
    try:
        # Send request
        response = requests.get(url=url, headers=headers, params=params)

        # Format request response
        if response.status_code == 200:
            orders = response.json()

            # Return data in JSON format
            return orders, 200
        else:

            # Return error if request failed (status code is not 200)
            return f"Failed to retrieve data: {response.status_code}", response.status_code
    except:
        return f"Failed to establish connection", 403