import datetime

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import JSON
import json


"""Start up the database"""
database = SQLAlchemy()


"""prediction_ids = id's used to make the financial prediction"""
class Predictions(database.Model):
    __tablename__ = 'predictions'
    id = database.Column(database.Integer, primary_key=True, auto_increment=True, nullable=False)
    start_time = database.Column(database.DateTime, nullable=False)
    end_time = database.Column(database.DateTime, nullable=False)
    prediction_ids = database.Column(database.JSON, nullable=False)

    def return_ids(self):
        return json.dumps(self.prediction_ids)


"""transaction_types = 'Employee', 'Stock', 'maintainence', 'overhead'"""
class Transactions(database.Model):
    __tablename__ = 'transactions'
    __table_args__ = (
        database.CheckConstraint("transaction_types IN ('Employee', 'Stock', 'maintainence', 'overhead')"),
    )
    id = database.Column(database.Integer, primary_key=True, auto_increment=True, nullable=False)
    date_time = database.Column(database.DateTime, nullable=False)
    transaction_types = database.Column(database.String, nullable=False)
    amount = database.Column(database.Integer, nullable=False)
    comment = database.Column(database.String, nullable=True)


"""Might not need this other than to store data on the frontend"""
class cookie(database.model):
    __tablename__ = 'transactions'
    id = database.Column(database.Integer, primary_key=True, nullable=False)
    cookie = database.Column(database.String, unique=True, nullable=False)
    delete_time = database.Column(database.DateTime, nullable=False)

    def is_deleted(self):
        return datetime.utcnow() > self.delete_time