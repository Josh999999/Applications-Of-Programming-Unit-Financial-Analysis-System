from flask import Flask, make_response, request, render_template
from app.database import *

app = Flask(__name__)

print(database)


"""Routes section"""


"""Main route"""
@app.route('/', methods = ['GET']) 
def getcookie(): 
    match request.method:
        case 'GET': 
            return 0


"""Cookie routes"""
@app.route('/setcookie', methods = ['POST', 'GET']) 
def setcookie():    
    match request.method:
        case 'GET': 
            name = request.cookies.get('userID') 
            return '<h1>welcome '+name+'</h1>'
        case 'POST':             
            user = request.form['nm'] 
            resp = make_response()
            resp.set_cookie('userID', user) 
            return resp

@app.route('/getcookie', methods = ['POST', 'GET']) 
def getcookie(): 
    match request.method:
        case 'GET': 
            name = request.cookies.get('userID') 
            return '<h1>welcome '+name+'</h1>'
        case 'POST': 
            return 'Done'


database.init_app(app)

with app.app_context():
    database.create_all()

if __name__ == '__main__':
    app.run(debug=True)