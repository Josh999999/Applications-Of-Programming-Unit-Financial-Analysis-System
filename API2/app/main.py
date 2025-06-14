from datetime import date
import rich
from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt
from app.complianceAndSecurityAPIHandler import check_ip_status, add_ip_to_blacklist, add_to_log, submit_data_access_request


"""Imports for the server setup"""
import flask
from app.routes import *
import os
import sys


"""Functions for setting up the server"""


def setUpServer(name: str, database_name: str, database, url_prefix: str) -> flask.Flask:
    app = flask.Flask(name)

    """Set up the ORM connected to the SQLite database"""
    database_relative_path = "../database/" + database_name
    app.config["SESSION_PERMANENTLY"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database_relative_path
        
    try: 
        # Initialize database inside the flask app
        database.init_app(app)
    except Exception as e:
        print("Couldn't initialize database, at: " + database_relative_path)
        sys.exit(1)

    # Get the routes from the blueprint set up in routes.py and return the app with the routes registered
    app.register_blueprint(routes_blueprint, url_prefix=URL_PREFIX)
    return app




"""Code for the rest of the flask setup"""

"""
# Setup console and prompt
console = Console()
prompt = Prompt()
"""


"""Present prompts for input on parameters used to run the API e.g. port, IP address, etc"""
"""
def handleUI(currentConsole: str, currentPrompt: str) -> dict:
    currentConsole.print("!---------------------------- The financial-Analysis-API is now running ----------------------------!", style="red bold underline")
    currentConsole.print("\n")
    currentConsole.print("You are now required enter the following API parameters \/", style="underline red")
    currentConsole.print("\n")

    host_ip_text = Text(text="* Host IP --> | default ==", style="underline green")
    host_port_text = Text(text="* Host Port --> | default ==", style="underline green")
    database_name_text = Text(text="* Database Name --> | default ==", style="underline green",)
    
    # Each variable takes in a default value (most likely use this value)
    host_ip = currentPrompt.ask(host_ip_text, default="127.0.0.1", show_default=True)    
    currentConsole.print("\n")
    host_port = currentPrompt.ask(host_port_text, default="5000", show_default=True)
    currentConsole.print("\n")
    database_name = currentPrompt.ask(database_name_text, default="financial_database.db", show_default=True)

    if database_name.count(".") < 1:
        database_name = database_name + ".db"

    # Args used in compiling the flask app
    args = {
        'host_ip': host_ip,
        'host_port': host_port,
        'database_name': database_name
    }

    return args


# Run UI function to get parameters for flask server
args = handleUI(console, prompt)

# GET parameters
host_ip = args['host_ip']
host_port = args['host_port']
database_name = args['database_name']
"""

# Set up flask app
app = setUpServer(__name__, "financial_database.db", database, url_prefix=URL_PREFIX)


"""Execution / preproccing before any requests starts to be processed"""
@app.before_request
def before_request() -> flask.json:   
    if (not request.method == 'OPTIONS'):
        # Check if address is in blacklist
        #ip_address = "10.0.0.5" # Cant use localhost address so use static address for the moment (to get request ip use - request.remote_addr)
        #ip_address = "10.0.0.2" # Use this to test the IP blacklist        
        ip_address = request.remote_addr

        """
        # Comment out complince and security checks to run web app
        ip_check_response = check_ip_status(ip_address)

        if ip_check_response.get("Error"):
            return flask.jsonify(ip_check_response.get("Error")), 500
        
        if ip_check_response.get("status") == 'blacklisted':
            return flask.jsonify({'Error': "Access denied: Requests given Ip Adress is blacklisted"}), 403 # 403 means forbidden
        """
        
            
        # GET API key from environment variables
        API_KEY = os.getenv('API_KEY')
        # Temp keep api key here statically and get from .env file when run in docker
        #API_KEY = "L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz"

        # Check if the method is OPTIONS (preflight request) - Used for CORS
        if request.method == 'OPTIONS':

            # You can manually add headers for OPTIONS requests here if needed - Filter IP addresses and allowed request types, etc
            response = app.make_response('')
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

        # Make sure path start with financial analysis system shorthand
        if request.path.startswith(URL_PREFIX):

            # Get authorization variable and assert that it's the API key
            auth_header = request.headers.get('Authorization')

            if auth_header !=API_KEY:
                # Log to security system if IP gives unauthorized request
                event = "Unauthorised IP"
                request_url = request.url
                request_method = request.method
                outcome = "Unauthorized request rejected and logged"
                add_to_log(event, ip_address, request_url, request_method, outcome)

                return flask.jsonify({'error': 'Request not authorised: Incorrect API key'}), 403 # 403 means forbidden
        else:
            return flask.jsonify({'error': 'Incorrect path prefix'}), 401
        
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response


"""Run the flask application"""
if __name__ == '__main__':
    #app.run(debug=True, host=host_ip, port=host_port)
    app.run(debug=True)



"""Preprocessing before the flask application is used - Mainly used for testing"""
with app.app_context():
    """Create the tables"""
    database.drop_all()
    database.create_all()

    """Add dumy query data - Leave this in as defualt queries"""
    """user_id in Financial analysis systems API and web interface defaults to 1 untill it is connected with authentication system"""
    """Eventually make the dummy data insert a process applied to each user after login - when there are no other queries present"""

    # Add new entries:
    new_ordering_report_query = ordering_report_query(
        name = 'query1',
        user_id = 1,
        start_time = date(2024, 12, 13),
        end_time = date(2025, 5, 31)
    )
    database.session.add(new_ordering_report_query)


    new_ordering_items_report_query = ordering_items_report_query(
        name = 'query1',
        user_id = 1,
        start_time = date(2024, 12, 13),
        end_time = date(2025, 5, 31)
    )
    database.session.add(new_ordering_items_report_query)

    
    new_ordering_graph_query = ordering_graph_query(
        name = 'query1',
        user_id = 1,
        start_time = date(2024, 12, 13),
        end_time = date(2025, 5, 31)
    )
    database.session.add(new_ordering_graph_query)


    new_ordering_items_graph_query = ordering_items_graph_query(
        name = 'query1',
        user_id = 1,
        start_time = date(2024, 12, 13),
        end_time = date(2025, 5, 31)
    )
    database.session.add(new_ordering_items_graph_query)

        
    database.session.commit()