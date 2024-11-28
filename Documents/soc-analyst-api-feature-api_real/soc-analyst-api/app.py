from flask import Flask, jsonify, request
from flask_cors import CORS  
import logging
import os
from api.login.main import main_func as login
from api.signup.main import main_func as signup
from api.cases_list.main import main_func as cases_list
from api.case_by_id.main import main_func as case_by_id
from api.get_progress_count.main import main_func as progress_count
from api.genai_model.main import main_func as genai_model

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

@app.route('/login', methods=['POST'])
def login_route():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Options OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        return response
    elif request.method == 'POST':
        return login()
    
@app.route('/cases_list', methods=['GET'])
def cases_list_route():
    return cases_list()

# xs430-rohmis ->

@app.route("/cases_list/<id>", methods=["GET"])
def get_case_by_id(id):
    print("indside get_case_by_id")
    return case_by_id()

@app.route("/alertcount", methods=["GET"])
def get_progress_count():
    print("indside alertcount")
    return progress_count()
  
# xs430-rohmis ->

@app.route('/signup', methods=['POST'])
def signup_route():
    return signup()

@app.route("/query", methods=['POST'])
def query_agent():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Options OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    elif request.method == 'POST':
        return genai_model()
        
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
