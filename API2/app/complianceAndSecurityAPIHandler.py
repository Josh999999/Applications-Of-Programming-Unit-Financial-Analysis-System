import requests
#from dotenv import load_dotenv
import os


"""Get neccessary variables"""  
# Get Security key for security API from environment variables
SECURITY_KEY = os.getenv("SECURITY_KEY")
# Security key here statically and get from .env file when run in docker
#SECURITY_KEY = "d8c7f1a4-35b2-497f-939a-ae462bf3d7c9"

#load_dotenv()

BASE_URL = "http://compliance-security-system:3000/api"


def check_ip_status(ip_address):
    """
    Calls the IP Check API to verify if an IP address is blacklisted.
    Args:
        ip_address (str): The IP address to check.
    Returns:
        dict: The response from the API as a dictionary.
    """
    url = f"{BASE_URL}/security/ipcheck"
    headers = {
        "X-Security-Key": SECURITY_KEY
    }
    params = {
        "ip": ip_address
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an Error for bad HTTP status codes
        return response.json()  # Parse the response JSON
    except requests.exceptions.RequestException as e:
        return {"Error": f"Request failed: {str(e)}"}


def add_ip_to_blacklist(ip_address):
    """
    Calls the Add IP to Blacklist API.
    Args:
        ip_address (str): The IP address to be added to the blacklist.
    Returns:
        dict: The response from the API as a dictionary.
    """
    url = f"{BASE_URL}/security/blacklist/add"
    headers = {
        "Content-Type": "application/json",
        "X-Security-Key": SECURITY_KEY
    }
    payload = {
        "ip": ip_address
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an Error for bad HTTP status codes
        return response.json()  # Parse the response JSON
    except requests.exceptions.RequestException as e:
        return {"Error": f"Request failed: {str(e)}"}
    

def add_to_log(event_type, ip_address, url_attempted, method, outcome, username=None, additional_info=None):
    """
    Calls the Add to Log API.
    Args:
        event_type (str): Type of the event (e.g., login_attempt, data_access).
        ip_address (str): The IP address of the requestor.
        url_attempted (str): The URL that was accessed or attempted.
        method (str): The HTTP method used (e.g., GET, POST).
        outcome (str): The outcome of the event (e.g., success, failure).
        username (str, optional): The username associated with the event.
        additional_info (str, optional): Any additional information related to the event.
    Returns:
        dict: The response from the API as a dictionary.
    """
    url = f"{BASE_URL}/security/log"
    headers = {
        "Content-Type": "application/json",
        "X-Security-Key": SECURITY_KEY
    }
    payload = {
        "eventType": event_type,
        "ipAddress": ip_address,
        "urlAttempted": url_attempted,
        "method": method,
        "outcome": outcome
    }

    if username:
        payload["username"] = username
    if additional_info:
        payload["additionalInfo"] = additional_info

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an Error for bad HTTP status codes
        return response.json()  # Parse the response JSON
    except requests.exceptions.RequestException as e:
        return {"Error": f"Request failed: {str(e)}"}
    

def submit_data_access_request(user_id, email):
    """
    Calls the Data Request API to submit a data access request.
    Args:
        user_id (str): The username submitting the request.
        email (str): The email address associated with the request.
    Returns:
        dict: The response from the API as a dictionary.
    """
    url = f"{BASE_URL}/compliance/data-requests/add"
    headers = {
        "Content-Type": "application/json",
        "X-Security-Key": SECURITY_KEY
    }
    payload = {
        "userId": user_id,
        "requestData": {
            "email": email
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an Error for bad HTTP status codes
        return response.json()  # Parse the response JSON
    except requests.exceptions.RequestException as e:
        return {"Error": f"Request failed: {str(e)}"}