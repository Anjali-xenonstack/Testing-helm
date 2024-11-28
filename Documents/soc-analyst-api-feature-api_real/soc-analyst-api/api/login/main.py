from flask import jsonify, request
import logging
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import database_connection
from .utility import login

logging.basicConfig(level=logging.INFO)

def init():
    conn = database_connection.check_db_connection()
    if conn is False:
        logging.error('check_db_connection returned False. retrying')
        return jsonify({'message': 'Database connection check failed', 'error': True}), 500

    if conn is True:
        logging.info('check_db_connection returned None. Attempting to establish connection.')
        conn = database_connection.connect_to_db()

        if conn is None:
            logging.error('connect_to_db returned None. Database connection failed.')
            return jsonify({'message': 'Database connection failed', 'error': True}), 500
        else:
            logging.info('Database connection established successfully.')
    logging.info(conn)
    return conn

def main_func():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password =  data.get('password')
        print(email, password)
        try:
            conn = init()
            if conn is None:
                return jsonify({'message': 'Database connection failed', 'error': True}), 500
            output, status_code = login.login_func(conn, email, password)
            return jsonify(output), status_code
        except Exception as e:
            logging.error(str(e))
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
