import logging
import os
import sys
from flask import jsonify, request
from .utility import logout

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
    if request.method == 'PUT':
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": True, "message": "Token is missing"}), 401
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
        else:
            token = auth_header
        try:
            conn = init()
            if conn is None:
                return jsonify({'message': 'Database connection failed', 'error': True}), 500
            email, token_response = decode_andfetch_user_id.decode_jwt_token(token)
            print("sdsdsdsdssd",email)
            if token_response == 200:
                output, status_code = logout.logout_func(conn, token, email)
                if output is not None:
                    return jsonify(output), status_code
                else:
                    return jsonify({'message': 'Internal server error', 'error': True}), 500
            if token_response != 200:
                return jsonify({'message': email, 'error': True}), token_response
        except Exception as e:
            return jsonify({"message": str(e), "error": True}), 500
    else:
        return jsonify({
            'message': '405 Method Not Allowed',
            'error': True,
        }), 405
