import flask
import requests as requests
from flask import request, send_from_directory, abort
from flask_cors import cross_origin
from app.database import database, ordering_report_query, ordering_items_report_query, ordering_graph_query, ordering_items_graph_query
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
import os
from app.orderManagementAPIHandler import get_orders, get_order_items

# Graphing dependencies
import pandas
import matplotlib
import seaborn


"""Get neccessary variables"""  
# GET URL prefix from environment variables
URL_PREFIX = os.getenv('URL_PREFIX')
# Temp URL prefix here statically and get from .env file when run in docker
#URL_PREFIX = "/finas/"


routes_blueprint = flask.Blueprint("routesAPI", __name__)


"""Routes section"""



"""Cookie routes - Not implemented with the authorization system yet"""
"""
@routes_blueprint.route('/setcookie', methods = ['POST'])
@cross_origin(supports_credentials=True)
def setcookie():    
    match request.method:
        case 'POST':             
            user = request.form['nm'] 
            resp = make_response()
            resp.set_cookie('userID', user) 
            return resp


@routes_blueprint.route('/getcookie', methods = ['POST', 'GET'])
@cross_origin(supports_credentials=True)
def getcookie(): 
    match request.method:
        case 'GET': 
            name = request.cookies.get('userID') 
            if not name:
                name = "default"
            returnText = '<h1>welcome '+name+'</h1>'
            returnJSON = '{"returnText" : "' + returnText + '"}'
            return json.loads(returnJSON)
        case 'POST': 
            return 'Done'
"""




"""Routes for the main functionality of the financial analysis system"""

"""
--- Details about file ---

All routes are given the "cross_origin()" to prevent CORS interuptions of requests - uneccessary as we hand IP restrictions through the security system API

"""


@routes_blueprint.route('/orders', methods = ['GET'])
@cross_origin()
def getOrders() -> flask.json:
    """
    Endpoint to fetch all orders in a date range.
    
    Returns:
        Response: A JSON response with the list of all orders in a date range.        
    """

    #Read in the parameters - str around dates for saftey when processing them
    data = request.args
    start_date = str(data['start_date'])
    end_date = str(data['end_date'])

    try:
        orders, status_code = get_orders(start_date, end_date)
        
    except Exception as e:
        return flask.jsonify({"Error": str(e) }), 500
    
    if status_code != 200:
        return flask.jsonify({'Error': orders}), status_code
    else:
        return flask.jsonify(orders), 200
    

@routes_blueprint.route('/orders/graph', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getOrdersGraph() -> flask.json:
    """
    Endpoint to fetch all orders in a date range and return graph based on the information.
    
    Returns:
        Response: An Image response displaying a graph of how much money was made through orders each month in the given range.        
    """
    
    #Read in the parameters - str around dates for saftey when processing them
    data = request.args
    start_date = str(data['start_date'])
    end_date = str(data['end_date'])
    user_id = int(data['user_id'])
    orders = ""

    try:
        orders, status_code = get_orders(start_date, end_date)

        # If isGraph return a graph created from the orders
        # If status_code != 200 then theres almost definitely no data in orders to create the graph with
        if status_code == 200:

            # Keep for display
            org_start_date = start_date
            org_end_date = end_date

            # Preprocess the order data before creating the graph
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date(),
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date(),

            # Access issue with datatime object have to index at 0
            start_date = start_date[0]
            end_date = end_date[0]

            # Get month difference between start and end:
            month_diff = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

            # Generate month start dates within the range
            month_ranges = []

            for i in range(0, month_diff + 1):
                if i == 0:
                    # If it's start date just get the last day of the month for the range
                    start_month_end_day = calendar.monthrange(start_date.year, start_date.month)[1] # Gets the last day of the month (1 for month in index)
                    start_date_end = start_date.replace(day=start_month_end_day)

                    start_date_str = start_date.strftime("%Y-%m-%d")
                    start_date_end_str = start_date_end.strftime("%Y-%m-%d")
                    
                    month_ranges.append((start_date_str, start_date_end_str))

                elif i == month_diff:
                    # If it's end date just get the first day of the month for the range
                    end_date_start = end_date.replace(day=1) # Set to first day of month

                    end_date_str = end_date.strftime("%Y-%m-%d") # Convert back for display purposes
                    end_date_start_str = end_date_start.strftime("%Y-%m-%d")
                    
                    month_ranges.append((end_date_start_str, end_date_str))

                else:
                    # Find the the first and last day of the month
                    next_month_date = start_date + relativedelta(months=i) # Get next month based on position (i away) from start date
                    next_month_date_start = next_month_date.replace(day=1) # Set to first day of month

                    next_month_end_day = calendar.monthrange(next_month_date.year, next_month_date.month)[1] # Gets the last day of the month
                    next_month_date_end = next_month_date.replace(day=next_month_end_day)

                    next_month_date_start_str = next_month_date_start.strftime("%Y-%m-%d") # Convert back for display purposes
                    next_month_date_end_str = next_month_date_end.strftime("%Y-%m-%d")

                    month_ranges.append((next_month_date_start_str, next_month_date_end_str))

            
            # load data into dataframe for easier analysis
            orders_dataframe = pandas.DataFrame(orders)

            # Remove time attribute from dates 
            #return flask.jsonify(orders_dataframe['order_date'][0]), status_code
        
            orders_dataframe['order_date'] = [str(order_date).split(' ')[0] for order_date in orders_dataframe['order_date']]
            
            #return flask.jsonify(orders_dataframe['order_date'][0]), status_code

            orders_dataframe['order_date'] = pandas.to_datetime(orders_dataframe['order_date'], format='%Y-%m-%d').dt.date

            month_range_quantities = [] # Y-axis
            x_names = [] # X-axis

            # Find the quantity of orders for each month range
            for month_range in month_ranges:

                # Query the dataframe to find orders in the current month range
                orders_dataframe_dateFilter = orders_dataframe.loc[
                    (orders_dataframe["order_date"] >= datetime.strptime(month_range[0], '%Y-%m-%d').date())
                    & (orders_dataframe["order_date"] <= datetime.strptime(month_range[1], '%Y-%m-%d').date())
                ]

                month_range_quantities.append(len(orders_dataframe_dateFilter))

                # Create name display for month range
                x_names.append(month_range[0] + " - " + month_range[1])

            plt = matplotlib.pyplot
            plt.rc('axes', titlesize=18)     # fontsize of the axes title
            plt.rc('axes', labelsize=14)     # fontsize of the x and y labels
            plt.rc('xtick', labelsize=13)    # fontsize of the tick labels
            plt.rc('ytick', labelsize=13)    # fontsize of the tick labels
            plt.rc('legend', fontsize=13)    # legend fontsize
            plt.rc('font', size=13)          # General font size
            seaborn.set_style('darkgrid')    # darkgrid, white grid, dark, white and ticks
            seaborn.color_palette("deep")    # Select color palette

            plt.figure(figsize=(2.8 * len(x_names), 1 * len(x_names)), tight_layout=True)
            ax = seaborn.barplot(x=x_names, y=month_range_quantities, palette='pastel')
            title = 'Order quantity per month from: ' + org_start_date + " to " + org_end_date
            ax.set(title=title, xlabel='Month ranges', ylabel='Number of orders',)

            # Save image temporarily to image directory
            iamgePath = f'app/tempImageStore/plot{user_id}.png'
            plt.savefig(iamgePath)

            # Cant call os module inside route for some reason
            try:
                return send_from_directory('tempImageStore', f'plot{user_id}.png', mimetype='image/gif')
            except Exception:

                # If exception likely image wasn't found
                abort(404, description="Image not found")
        
    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    if status_code != 200:
        return flask.jsonify({'Error': orders}), status_code
    else:
        return flask.jsonify(orders), 200


@routes_blueprint.route('/orders/items', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getOrdersItems() -> flask.json:
    """
    Endpoint to fetch all items and quantity of them over orders in a date range.
    
    Returns:
        Response: A JSON response with the list of all items and quantity of them over orders in a date range.        
    """
    
    #Read in the parameters - str around dates for saftey when processing them
    data = request.args
    start_date = str(data['start_date'])
    end_date = str(data['end_date'])

    try:
        items, status_code = get_order_items(start_date, end_date)
        
    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    if status_code != 200:
        return flask.jsonify({'Error': items}), status_code
    else:
        return flask.jsonify(items), 200
    

@routes_blueprint.route('/orders/items/graph', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getOrdersItemsGraph() -> flask.json:  
    """
    Endpoint to fetch all items and quantity of them over orders in a date range and return graph based on the information.
    
    Returns:
        Response: A Iamge displaying a graph showing how much individual items were ordered over a given date range.        
    """
    
    #Read in the transactions - str around dates for saftey when processing them
    #TODO() - Add user_id to image then delete it (instead of overwrite) after to save space
    data = request.args
    start_date = str(data['start_date'])
    end_date = str(data['end_date'])
    user_id = int(data['user_id'])
    items = ""

    try:
        items, status_code = get_order_items(start_date, end_date)

        # If isGraph return a graph created from the orders
        # If status_code != 200 then theres almost definitely no data in orders to create the graph with
        if status_code == 200:

            plt = matplotlib.pyplot
            plt.rc('axes', titlesize=18)     # fontsize of the axes title
            plt.rc('axes', labelsize=14)     # fontsize of the x and y labels
            plt.rc('xtick', labelsize=13)    # fontsize of the tick labels
            plt.rc('ytick', labelsize=13)    # fontsize of the tick labels
            plt.rc('legend', fontsize=13)    # legend fontsize
            plt.rc('font', size=13)          # General font size
            seaborn.set_style('darkgrid')    # darkgrid, white grid, dark, white and ticks
            seaborn.color_palette("deep")    # Select color palette

            # Get lists of names and quantities from each object        
            items_names = [item["name"] for item in items]
            items_quantity = [item["quantity"] for item in items]

            plt.figure(figsize=(2 * len(items_names), 1 * len(items_names)), tight_layout=True)
            ax = seaborn.barplot(x=items_names, y=items_quantity, palette='pastel')
            title = 'Item order quantity from: ' + start_date + " to " + end_date
            ax.set(title=title, xlabel='Items', ylabel='Order quantity',)

            # Save image temporarily to image directory
            plt.savefig(f'app/tempImageStore/plot{user_id}.png')

            # Cant call os module inside route
            try:
                return send_from_directory('tempImageStore', f'plot{user_id}.png', mimetype='image/gif')
            except Exception:

                # If exception likely image wasn't found
                abort(404, description="Image not found")
        
    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    if status_code != 200:
        return flask.jsonify({'Error': items}), status_code
    else:
        return flask.jsonify(items), 200



"""GET Routes for each type of query"""

"""
The routes here determine the "type" parameter returned by each query - determines which type integer a query is assinged to (this information is not kept in the database)

The "type" parameter is given as a means of determining which type of query you are interacting with

The type parameter is given here as storing it in the database is a violation of RBDMS rules against redundancy of colums
(all type data would be the same integer as different query types are kept in different database tables - reference database.py for more details)
"""

@routes_blueprint.route('/user/query/orderingReport', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getUserQueryOrderingReport() -> flask.json:
    """
    Endpoint to fetch an orderingReport queries
    
    Returns:
        Response: A JSON object containing the selected orderingReport query
    """
    # Read in the parameters
    data = request.args
    user_id = int(data['user_id'])
    id = int(data['id'])
    
    try:
        # filter by id and user_id so users can't select any query that doesn't belong to them
        ordering_report_queries = database.session.execute(database.select(ordering_report_query).filter_by(user_id=user_id, id=id)).scalars().all()
    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    # Run through the SQLAlchemyQueryObjectToJSONAcceptable allowing for more than one query
    ordering_report_queries = [SQLAlchemyQueryObjectToJSONAcceptable(ordering_report_query, type=1, isGraph=False) for ordering_report_query in ordering_report_queries]

    return flask.jsonify(ordering_report_queries), 200


@routes_blueprint.route('/user/query/orderingItemReport', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getUserQueryOrderingItemReport() -> flask.json:
    """
    Endpoint to fetch an orderingItemReport queries
    
    Returns:
        Response: A JSON object containing the selected orderingItemReport query
    """

    #Read in the parameters
    data = request.args
    user_id = int(data['user_id'])
    id = int(data['id'])
    
    try: 
        # filter by id and user_id so users can't select any query that doesn't belong to them
        ordering_items_report_queries = database.session.execute(database.select(ordering_items_report_query).filter_by(user_id=user_id, id=id)).scalars().all()
    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    # Run through the SQLAlchemyQueryObjectToJSONAcceptable allowing for more than one query
    ordering_items_report_queries = [SQLAlchemyQueryObjectToJSONAcceptable(ordering_items_report_query, type=2, isGraph=False) for ordering_items_report_query in ordering_items_report_queries]

    return flask.jsonify(ordering_items_report_queries), 200


@routes_blueprint.route('/user/query/orderingGraph', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getUserQueryOrderingGraph() -> flask.json:
    """
    Endpoint to fetch an orderingGraph queries
    
    Returns:
        Response: A JSON object containing the selected orderingGraph query
    """

    # Read in the parameters
    data = request.args
    user_id = int(data['user_id'])
    id = int(data['id'])
    
    try: 
        # filter by id and user_id so users can't select any query that doesn't belong to them
        ordering_graph_queries = database.session.execute(database.select(ordering_graph_query).filter_by(user_id=user_id, id=id)).scalars().all()
    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    # Run through the SQLAlchemyQueryObjectToJSONAcceptable allowing for more than one query
    ordering_graph_queries = [SQLAlchemyQueryObjectToJSONAcceptable(ordering_graph_query, type=3, isGraph=True) for ordering_graph_query in ordering_graph_queries]

    return flask.jsonify(ordering_graph_queries), 200


@routes_blueprint.route('/user/query/orderingItemGraph', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getUserQueryOrderingItemGraph() -> flask.json:
    """
    Endpoint to fetch an orderingItemGraph queries
    
    Returns:
        Response: A JSON object containing the selected orderingItemGraph query
    """
    # Read in the parameters
    data = request.args
    user_id = int(data['user_id'])
    id = int(data['id'])
    
    try: 
        # filter by id and user_id so users can't select any query that doesn't belong to them
        ordering_items_graph_queries = database.session.execute(database.select(ordering_items_graph_query).filter_by(user_id=user_id, id=id)).scalars().all()
    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    # Run through the SQLAlchemyQueryObjectToJSONAcceptable allowing for more than one query
    ordering_items_graph_queries = [SQLAlchemyQueryObjectToJSONAcceptable(ordering_items_graph_query, type=4, isGraph=True) for ordering_items_graph_query in ordering_items_graph_queries]

    return flask.jsonify(ordering_items_graph_queries), 200


"""Route to return all queries of every type"""
@routes_blueprint.route('/user/queries', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getUserQueries() -> flask.json:
    """
    Endpoint to fetch all user queries
    
    Returns:
        Response: A JSON object containing all the parameters of users queries
    """
    # Read in the parameters
    data = request.args
    user_id = int(data['user_id'])
    
    try: 
        # SELECT every type of query
        ordering_report_queries = database.session.execute(database.select(ordering_report_query).filter_by(user_id=user_id)).scalars().all()
        ordering_items_report_queries = database.session.execute(database.select(ordering_items_report_query).filter_by(user_id=user_id)).scalars().all()
        ordering_graph_queries = database.session.execute(database.select(ordering_graph_query).filter_by(user_id=user_id)).scalars().all()
        ordering_items_graph_queries = database.session.execute(database.select(ordering_items_graph_query).filter_by(user_id=user_id)).scalars().all()
    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    ordering_report_queries = [SQLAlchemyQueryObjectToJSONAcceptable(ordering_report_query, type=1, isGraph=False) for ordering_report_query in ordering_report_queries]

    ordering_items_report_queries = [SQLAlchemyQueryObjectToJSONAcceptable(ordering_items_report_query, type=2, isGraph=False) for ordering_items_report_query in ordering_items_report_queries]

    ordering_graph_queries = [SQLAlchemyQueryObjectToJSONAcceptable(ordering_graph_query, type=3, isGraph=True) for ordering_graph_query in ordering_graph_queries]

    ordering_items_graph_queries = [SQLAlchemyQueryObjectToJSONAcceptable(ordering_items_graph_query, type=4, isGraph=True) for ordering_items_graph_query in ordering_items_graph_queries]

    queries = ordering_report_queries + ordering_items_report_queries + ordering_graph_queries + ordering_items_graph_queries

    return flask.jsonify(queries), 200




"""POST routes to create new queries"""

"""Possibly return information the created queries attempt to retrieve in the future"""
@routes_blueprint.route('/user/query/orderingReport', methods = ['POST'])
@cross_origin(supports_credentials=True)
def postOrdersReport() -> flask.json:
    """
    Endpoint to create an orderingReport queries
    
    Returns:
        Response: A JSON response (message) on the status of the request
    """
    
    # Read in the request body
    data = request.get_json()
    start_date = str(data['start_date'])
    end_date = str(data['end_date'])
    user_id = int(data['user_id'])
    name = str(data['name'])

    try:
        # INSERT into the database via the ORM
        new_ordering_report_query = ordering_report_query(
            user_id = user_id,
            name = name,
            start_time = datetime.strptime(start_date.replace("/", ""), '%d%m%Y').date(),
            end_time = datetime.strptime(end_date.replace("/", ""), '%d%m%Y').date(), 
        )
        
        database.session.add(new_ordering_report_query)
        database.session.commit()

    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    return flask.jsonify({'Complete': "New queries created"}), 200


@routes_blueprint.route('/user/query/orderingItemReport', methods = ['POST'])
@cross_origin(supports_credentials=True)
def postOrdersItemsReport() -> flask.json:
    """
    Endpoint to create an OrdersItemsReport queries
    
    Returns:
        Response: A JSON response (message) on the status of the request
    """
    
    # Read in the request body
    data = request.get_json()
    start_date = str(data['start_date'])
    end_date = str(data['end_date'])
    user_id = int(data['user_id'])
    name = str(data['name'])

    try:
        # INSERT into the database via the ORM
        new_ordering_items_report_query = ordering_items_report_query(
            user_id = user_id,
            name = name,
            start_time = datetime.strptime(start_date.replace("/", ""), '%d%m%Y').date(),
            end_time =  datetime.strptime(end_date.replace("/", ""), '%d%m%Y').date(), 
        )
        
        database.session.add(new_ordering_items_report_query)
        database.session.commit()

    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    return flask.jsonify({'Complete': "New queries created"}), 200


@routes_blueprint.route('/user/query/orderingGraph', methods = ['POST'])
@cross_origin(supports_credentials=True)
def postOrdersGraph() -> flask.json:
    """
    Endpoint to create an OrdersGraph queries
    
    Returns:
        Response: A JSON response (message) on the status of the request
    """
    
    # Read in the request body
    data = request.get_json()
    start_date = str(data['start_date'])
    end_date = str(data['end_date'])
    user_id = int(data['user_id'])
    name = str(data['name'])

    try:
        # INSERT into the database via the ORM
        new_ordering_graph_query = ordering_graph_query(
            user_id = user_id,
            name = name,
            start_time = datetime.strptime(start_date.replace("/", ""), '%d%m%Y').date(),
            end_time =  datetime.strptime(end_date.replace("/", ""), '%d%m%Y').date(), 
        )
        
        database.session.add(new_ordering_graph_query)
        database.session.commit()

    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    return flask.jsonify({'Complete': "New queries created"}), 200


@routes_blueprint.route('/user/query/orderingItemGraph', methods = ['POST'])
@cross_origin(supports_credentials=True)
def postOrdersItemsGraph() -> flask.json:
    """
    Endpoint to create an OrdersItemsGraph queries
    
    Returns:
        Response: A JSON response (message) on the status of the request
    """
    
    # Read in the request body
    data = request.get_json()
    start_date = str(data['start_date'])
    end_date = str(data['end_date'])
    user_id = int(data['user_id'])
    name = str(data['name'])

    try:
        # INSERT into the database via the ORM
        new_ordering_items_graph_query = ordering_items_graph_query(
            user_id = user_id,
            name = name,
            start_time = datetime.strptime(start_date.replace("/", ""), '%d%m%Y').date(),
            end_time =  datetime.strptime(end_date.replace("/", ""), '%d%m%Y').date(), 
        )
        
        database.session.add(new_ordering_items_graph_query)
        database.session.commit()

    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    return flask.jsonify({'Complete': "New queries created"}), 200




"""DELETE routes to delete queries"""
"""Possibly return information of the deleted queries in the future"""
@routes_blueprint.route('/user/query/orderingReport', methods = ['DELETE'])
@cross_origin(supports_credentials=True)
def deleteOrdersReport() -> flask.json:
    """
    Endpoint to remove orderingReport queries with given id 
    
    Returns:
        Response: A JSON response (message) on the status of the request
    """
    
    #Read in the parameters
    data = request.args
    id = int(data['id'])
    user_id = int(data['user_id'])

    try:
        # filter by id and user_id so users can't delete any query that doesn't belong to them
        ordering_report_queries = database.session.execute(database.select(ordering_report_query).filter_by(user_id=user_id, id=id)).scalars().all()
        database.session.delete(ordering_report_queries[0])
        database.session.commit()

    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    return flask.jsonify({'Complete': "Query deleted"}), 200


@routes_blueprint.route('/user/query/orderingGraph', methods = ['DELETE'])
@cross_origin(supports_credentials=True)
def deleteOrdersGraph() -> flask.json:
    """
    Endpoint to remove orderingGraph queries with given id 
    
    Returns:
        Response: A JSON response (message) on the status of the request
    """

    # Blacklist = 403
    
    #Read in the transactions
    data = request.args
    id = int(data['id'])
    user_id = int(data['user_id'])

    try:
        # filter by id and user_id so users can't delete any query that doesn't belong to them
        ordering_graph_queries = database.session.execute(database.select(ordering_graph_query).filter_by(user_id=user_id, id=id)).scalars().all()
        database.session.delete(ordering_graph_queries[0])
        database.session.commit()

    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    return flask.jsonify({'Complete': "Query deleted"}), 200


@routes_blueprint.route('/user/query/orderingItemReport', methods = ['DELETE'])
@cross_origin(supports_credentials=True)
def deleteOrdersItemsReport() -> flask.json:
    """
    Endpoint to remove orderingItemReport queries with given id 
    
    Returns:
        Response: A JSON response (message) on the status of the request
    """
    
    #Read in the transactions
    data = request.args
    id = int(data['id'])
    user_id = int(data['user_id'])

    try:
        # filter by id and user_id so users can't delete any query that doesn't belong to them
        ordering_items_report_queries = database.session.execute(database.select(ordering_items_report_query).filter_by(user_id=user_id, id=id)).scalars().all()
        database.session.delete(ordering_items_report_queries[0])
        database.session.commit()

    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    return flask.jsonify({'Complete': "Query deleted"}), 200


@routes_blueprint.route('/user/query/orderingItemGraph', methods = ['DELETE'])
@cross_origin(supports_credentials=True)
def deleteOrdersItemsGraph() -> flask.json:
    """
    Endpoint to remove orderingItemGraph queries with given id 
    
    Returns:
        Response: A JSON response (message) on the status of the request
    """
    
    #Read in the transactions
    data = request.args
    id = int(data['id'])
    user_id = int(data['user_id'])

    try:
        # filter by id and user_id so users can't delete any query that doesn't belong to them
        ordering_items_graph_queries = database.session.execute(database.select(ordering_items_graph_query).filter_by(user_id=user_id)).scalars().all()
        database.session.delete(ordering_items_graph_queries[0])
        database.session.commit()

    except Exception as e:
        return flask.jsonify({'Error': str(e)}), 500
    
    return flask.jsonify({'Complete': "Query deleted"}), 200




"""Route to return the route for each query type as a lookup table"""
@routes_blueprint.route('/queries/lookup', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getQueriesLookup() -> flask.json:
    """
    Endpoint to fetch all the routes needed to make all possible requests to each type of query

    Indexes for the routes in this object match the "type" parameter returned by the GET request in each query based route so that knowing the type means knowing the route
    to DELETE, GET or POST the required query
    
    Returns:
        Response: A JSON response with an object containing all query routes for each type of request + names
    """
    
    #Read in the transactions
    # Makes sure indexes match up in all request types + names
    queriesLookup = {
        "GET":{
            0: URL_PREFIX + 'orders',
            1: URL_PREFIX + 'orders/items',
            2: URL_PREFIX + 'orders/graph',
            3: URL_PREFIX + 'orders/items/graph',
        },
        "DELETE":{
            0: URL_PREFIX + 'user/query/orderingReport',
            1: URL_PREFIX + 'user/query/orderingItemReport',
            2: URL_PREFIX + 'user/query/orderingGraph' ,
            3: URL_PREFIX + 'user/query/orderingItemGraph',
        },
        "POST":{
            0: URL_PREFIX + 'user/query/orderingReport',
            1: URL_PREFIX + 'user/query/orderingItemReport',
            2: URL_PREFIX + 'user/query/orderingGraph' ,
            3: URL_PREFIX + 'user/query/orderingItemGraph',
        },
        "queryNames": {
            0: 'Orders Report',
            1: 'Order Items Report',
            2: 'Orders Graps' ,
            3: 'Order Items Graph',
        },
    }
    
    return flask.jsonify(queriesLookup), 200








"""Functions used by the routes of this API"""

def SQLAlchemyQueryObjectToJSONAcceptable(queryObject, type: int, isGraph: bool) -> dict:
    """
    Takes in a query object returned from an SQLAlchemy query and converts it to a dictionary for JSON serialisation

    The function also adds the variables "type" and "isGraph" for data processing convenience and 
    context absolution (the one you assume is the graph type based on name, etc acutally is one)

    Returns dates in the standard format for this API "%Y-%m-%d"
    """

    newQueryObject = {
        "id": queryObject.id,
        "name": queryObject.name,
        "user_id": queryObject.user_id,
        "start_date": queryObject.start_time.strftime("%Y-%m-%d"),
        "end_date": queryObject.end_time.strftime("%Y-%m-%d"),
        "type": type,
        "isGraph": int(isGraph)
    }

    return newQueryObject
