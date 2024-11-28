import logging
import os
import sys
from flask import jsonify,request
from .utility import signup

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import database_connection, decode_andfetch_user_id  # noqa

logging.basicConfig(level=logging.INFO)

login_dbconnection = None


def init():
    global login_dbconnection
    if login_dbconnection is not None:
        logging.info('Database connection already established.')
        return login_dbconnection
    logging.error('Database connection not established. Retrying...')
    conn = database_connection.connect_to_db()

    if conn is None:
        logging.error('connect_to_db returned None. Database connection failed.')
        return None
    else:
        logging.info('Database connection established successfully. (init function)')
        login_dbconnection = conn
        return conn


def main_func():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password =  data.get('password')
        username =  data.get('name')
        if any(field is None for field in [email, username, password]):
            return jsonify({
                'message': 'wrong payload',
                'error': True,
            }), 405
        try:
            conn = init()
            if conn is None:
                return jsonify({'message': 'Database connection failed', 'error': True}), 500
            output, status_code = signup.signup_func(conn, email,username,password)
            return jsonify(output), status_code
        except Exception as e:
            logging.error(f"Error in main function: {str(e)}")
            return jsonify({
                'message': 'Internal server error',
                'error': True,
                'operation': 'main'
            }), 500
    else:
        return jsonify({
            'message': '405 Method Not Allowed',
            'error': True,
        }), 405
