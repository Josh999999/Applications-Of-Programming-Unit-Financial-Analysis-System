# Financial-Analysis-System

## Features:
  - **Querying** - Can use information stored by other systems to produce user parameterized queries to analyse the financial activities of the business
  - **Visualisation** - Provides a web solution to visualise the data returned from the API (displays both tables of data and graphs based on query data)
  - **Security** - Implements other systems such as Authentication and Compliance and security to ensure the security of the financial information

## Communication with other systems (planned and carried out)
1. [x] **Order Management system**
2. [ ] **Authentication system**
3. [X] **Compliance and security system**
4. [ ] **Logistics Management system**
5. [ ] **Payroll management system**


## System communication diagram
4. ![image](https://github.com/user-attachments/assets/159fe5cb-d35f-4f11-8313-e0ffd96b8b90)


---

# Running the API's
As it currently stands you will have to clone this repository to run it's docker containers. The dockerfile for the API and web app are located in the relevant folders respectively

## Running the Flask API
To reference the API in requests use the format 
```
"http://flask-api/finas/-rest of request-"
```
As this references the docker container and the API's prefix '/finas/'


1. To start with build the docker image - We create the image to run on localhost at port 5000
```
docker build -t financial-analysis-system
```

2. Next build the docker image for the systems currently integrated with the financial analysis system's API
```
docker build -t compliance-security-system
```
```
docker build -t ordermanagementsystem
```
```
docker build -t dummydataapi
```
If running any of these Images in the compose doesn't work for you they can be run seperatly

3. Create a shared docker network for these contains to communicate on:
```
docker network create shared_network
```

4. Run compose for the financial analysis system API
```
docker-compose up --build
```

## Running the Web Application
1. Make sure you have the financial analysis system's API already running

2. Next build the docker image
```
docker build -t financial-analysis-system-web-app
```
3. Create a shared docker network for these contains to communicate on:
```
docker network create shared_network
```
4. Run compose for the financial analysis system web app
```
docker-compose up --build
```

---

# Communicating with the API
When comminicating the with the API you need to use the prefix '/finas/' before all routes and put the following in the header
```
{ "Authorisation" : API_KEY }
```
You can configure you own API_KEY by changing the variable of the same name in the .env file

## Get the query type lookup dictionary
This can be used to find the type of route you are going to need to call based on the type of query you are dealing with.
### Request:
```
http://127.0.0.1:5000/finas/queries/lookup
```
### Response:
```
{
    "DELETE": {
        "0": "/finas/user/query/orderingReport",
        "1": "/finas/user/query/orderingItemReport",
        "2": "/finas/user/query/orderingGraph",
        "3": "/finas/user/query/orderingItemGraph"
    },
    "GET": {
        "0": "/finas/orders",
        "1": "/finas/orders/items",
        "2": "/finas/orders/graph",
        "3": "/finas/orders/items/graph"
    },
    "POST": {
        "0": "/finas/user/query/orderingReport",
        "1": "/finas/user/query/orderingItemReport",
        "2": "/finas/user/query/orderingGraph",
        "3": "/finas/user/query/orderingItemGraph"
    },
    "queryNames": {
        "0": "Orders Report",
        "1": "Order Items Report",
        "2": "Orders Graps",
        "3": "Order Items Graph"
    }
}
```


## Get the all of a users queries
This can be used to get all of the queries that belong to a given user
### Request:
```
http://0.0.0.0:5000/finas/user/queries?user_id=user_id
```
### Example Response:
```
[
    {
        "end_date": "2025-05-31",
        "id": 1,
        "isGraph": 0,
        "name": "query1",
        "start_date": "2024-12-13",
        "type": 1,
        "user_id": 1
    },
    {
        "end_date": "2025-05-31",
        "id": 1,
        "isGraph": 0,
        "name": "query1",
        "start_date": "2024-12-13",
        "type": 2,
        "user_id": 1
    },
]
```


## Get the OrderingReport query type
This can be used to get a OrderingReport query of a given type for a given user
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingReport?user_id=user_id&id=query_id
```
### Example Response:
```
[
    {
        "end_date": "2025-05-31",
        "id": 1,
        "isGraph": 0,
        "name": "query1",
        "start_date": "2024-12-13",
        "type": 1,
        "user_id": 1
    },
]
```

## Get the OrderingItemReport query type
This can be used to get a OrderingItemReport query of a given type for a given user
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingItemReport?user_id=user_id&id=query_id
```
### Example Response:
```
[
    {
        "end_date": "2025-05-31",
        "id": 1,
        "isGraph": 0,
        "name": "query1",
        "start_date": "2024-12-13",
        "type": 2,
        "user_id": 1
    },
]
```

## Get the OrderingGraph query type
This can be used to get a OrderingGraph query of a given type for a given user
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingGraph?user_id=user_id&id=query_id
```
### Example Response:
```
[
    {
        "end_date": "2025-05-31",
        "id": 1,
        "isGraph": 0,
        "name": "query1",
        "start_date": "2024-12-13",
        "type": 3,
        "user_id": 1
    },
]
```

## Get the OrderingItemGraph query type
This can be used to get a OrderingItemGraph query of a given type for a given user
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingItemGraph?user_id=user_id&id=query_id
```
### Example Response:
```
[
    {
        "end_date": "2025-05-31",
        "id": 1,
        "isGraph": 0,
        "name": "query1",
        "start_date": "2024-12-13",
        "type": 4,
        "user_id": 1
    },
]
```

## Get all orders in a given date range
This can be used to get a list of all order objects within a given date range
### Request:
```
http://localhost:5000/finas/orders?start_date=start_date&end_date=end_date
```
### Example Response:
```
[
    {
        "branch_id": 1002,
        "items": [
            {
                "item_id": 29,
                "modifications": "None",
                "quantity": "5"
            }
        ],
        "order_date": "2025-01-14 11:32:43",
        "order_id": 2,
        "order_type": "Eat In",
        "price": 11.16,
        "status": "PENDING",
        "table_number": 19,
        "user_id": "78"
    },
    {
        "branch_id": 1001,
        "items": [
            {
                "item_id": 2,
                "modifications": "",
                "quantity": "3"
            },
            {
                "item_id": 8,
                "modifications": "",
                "quantity": "1"
            },
            {
                "item_id": 20,
                "modifications": "",
                "quantity": "2"
            },
            {
                "item_id": 13,
                "modifications": "",
                "quantity": "3"
            }
        ],
        "order_date": "2025-01-14 11:32:44",
        "order_id": 3,
        "order_type": "Delivery",
        "price": 39.58,
        "status": "PENDING",
        "table_number": null,
        "user_id": "95"
    }
]
```


## Get all items order quantity in a given date range
This can be used to get a list of all items and their quantity of order over a given date range
### Request:
```
http://localhost:5000/finas/orders/items?start_date=start_date&end_date=end_date
```
### Example Response:
```
[
    {
        "description": "Glass of house white wine",
        "name": "White Wine",
        "price": 4.5,
        "quantity": 11
    },
    {
        "description": "Classic pizza topped with spicy pepperoni slices",
        "name": "Pepperoni Pizza",
        "price": 9.99,
        "quantity": 11
    }
]
```


## Get graph of order quantity in a given date range
This can be used to get a graph of order quantity in a given date range
### Request:
```
http://localhost:5000/finas/orders/graph?start_date=start_date&end_date=end_date&user_id=user_id
```
### Example Response:
```
![image](https://github.com/user-attachments/assets/4796aa00-d118-4c73-93bb-b3a0c39dcb24)
```


## Get graph of item order quantity in a given date range
This can be used to get a graph of item order quantity in a given date range
### Request:
```
http://127.0.0.1:5000/finas/orders/items/graph?start_date=start_date&end_date=end_date&user_id=user_id
```
### Example Response:
```
![image](https://github.com/user-attachments/assets/7b3650de-2f3b-4395-ab30-a8e25d48bfaa)
```


## Create a new query of OrderingReport query type
This can be used to provide the parameters needed to create a new query of OrderingReport query type
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingReport
```
### Body Example:
```
{
    "user_id": 1,
    "start_date": "12/12/2024",
    "end_date": "16/12/2024",
    "name": "NewQuery1"
}
```
### Response:
```
{
    "Complete": "New queries created"
}
```


## Create a new query of OrderingItemReport query type
This can be used to provide the parameters needed to create a new query of OrderingItemReport query type
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingItemReport
```
### Body Example:
```
{
    "user_id": 2,
    "start_date": "12/12/2024",
    "end_date": "16/12/2024",
    "name": "NewQuery1"
}
```
### Response:
```
{
    "Complete": "New queries created"
}
```


## Create a new query of OrderingGraph query type
This can be used to provide the parameters needed to create a new query of OrderingGraph query type
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingGraph
```
### Body Example:
```
{
    "user_id": 2,
    "start_date": "12/12/2024",
    "end_date": "16/12/2024",
    "name": "NewQuery1"
}
```
### Response:
```
{
    "Complete": "New queries created"
}
```


## Create a new query of OrderingItemGraph query type
This can be used to provide the parameters needed to create a new query of OrderingItemGraph query type
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingItemGraph
```
### Body Example:
```
{
    "user_id": 2,
    "start_date": "12/12/2024",
    "end_date": "16/12/2024",
    "name": "NewQuery1"
}
```
### Response:
```
{
    "Complete": "New queries created"
}
```


## Delete an existing query of OrderingReport query type
This can be used to delete an existing query of OrderingReport query type with a given id
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingReport?user_id=user_id&id=query_id
```
### Response:
```
{
    "Complete": "Query deleted"
}
```


## Delete an existing query of OrderingGraph query type
This can be used to delete an existing query of OrderingGraph query type with a given id
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingGraph?user_id=user_id&id=query_id
```
### Response:
```
{
    "Complete": "Query deleted"
}
```


## Delete an existing query of OrderingItemReport query type
This can be used to delete an existing query of OrderingItemReport query type with a given id
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingItemReport?user_id=user_id&id=query_id
```
### Response:
```
{
    "Complete": "Query deleted"
}
```


## Delete an existing query of OrderingItemGraph query type
This can be used to delete an existing query of OrderingItemGraph query type with a given id
### Request:
```
http://127.0.0.1:5000/finas/user/query/orderingItemGraph?user_id=user_id&id=query_id
```
### Response:
```
{
    "Complete": "Query deleted"
}
```
