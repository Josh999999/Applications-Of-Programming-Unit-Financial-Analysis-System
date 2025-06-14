from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


"""Start up the database"""
class Base(DeclarativeBase):
  pass

database = SQLAlchemy(model_class=Base)


"""Might not need this other than to store data on the frontend  - Not implemented with the authorization system yet"""
"""
class cookie(database.Model):
    # Table name:
    __tablename__ = 'cookies'
    id = database.Column(database.Integer, primary_key=True, nullable=False) # Primary key
    cookie = database.Column(database.String, unique=True, nullable=False)
    delete_time = database.Column(database.DateTime, nullable=False)

    # Table functions:
    def is_deleted(self):
        return datetime.timezone.utc() > self.delete_time
    

# Populate models to include in flask admin
dbModels = ["predictions", "predictions_W_transactions", "transaction_types", "transactions", "transaction_predictions"]
"""




"""Tables for the saving of financial queries made by the user"""

"""
Query types are kept inside tables for the purposes of scalability and expansion

Different query types may eventually have different attributes that require storage e.g. graph colors
"""

"""Ordering report query table"""
class ordering_report_query(database.Model):
    # Table name:
    __tablename__ = 'ordering_report_query'

    # Table columns:
    id = database.Column(database.Integer, primary_key=True, nullable=False) # Primary key
    name = database.Column(database.String, nullable=True)
    user_id = database.Column(database.Integer, nullable=False)
    start_time = database.Column(database.DateTime, nullable=False)
    end_time = database.Column(database.DateTime, nullable=False)
    

"""Ordering items report query table"""
class ordering_items_report_query(database.Model):
    # Table name:
    __tablename__ = 'ordering_items_report_query'

    # Table columns:
    id = database.Column(database.Integer, primary_key=True, nullable=False) # Primary key
    name = database.Column(database.String, nullable=True)
    user_id = database.Column(database.Integer, nullable=False)
    start_time = database.Column(database.DateTime, nullable=False)
    end_time = database.Column(database.DateTime, nullable=False)
    

"""Ordering graph query table"""
class ordering_graph_query(database.Model):
    # Table name:
    __tablename__ = 'ordering_graph_query'

    # Table columns:
    id = database.Column(database.Integer, primary_key=True, nullable=False) # Primary key
    name = database.Column(database.String, nullable=True)
    user_id = database.Column(database.Integer, nullable=False)
    start_time = database.Column(database.DateTime, nullable=False)
    end_time = database.Column(database.DateTime, nullable=False)
    

"""Ordering items graph query table"""
"""More attributes will likely be added to the graph query tables"""
class ordering_items_graph_query(database.Model):
    # Table name:
    __tablename__ = 'ordering_items_graph_query'

    # Table columns:
    id = database.Column(database.Integer, primary_key=True, nullable=False) # Primary key
    name = database.Column(database.String, nullable=True)
    user_id = database.Column(database.Integer, nullable=False)
    start_time = database.Column(database.DateTime, nullable=False)
    end_time = database.Column(database.DateTime, nullable=False)