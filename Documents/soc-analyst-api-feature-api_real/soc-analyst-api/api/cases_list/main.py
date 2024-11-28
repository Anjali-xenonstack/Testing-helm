from flask import jsonify, request
import logging
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import database_connection,decode_andfetch_user_id
from .utility import cases_list

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
    if request.method == 'GET':
        # auth_header = request.headers.get("Authorization")

        # if not auth_header:
        #     return jsonify({"error": True, "message": "Token is missing"}), 401
        # if auth_header.startswith("Bearer "):
        #     token = auth_header.replace("Bearer ", "")
        # else:
        #     token = auth_header
        try:
            print("hello1")
            # _,status =decode_andfetch_user_id.decode_jwt_token(token)
            # if status != 200: 
            #     return jsonify({"error": True, "message": "Unauthorized access"}), 401
            case_type = request.args.get("type")
            alert_type = request.args.get("alert_type")
            page = request.args.get("page")

            print(page,"this is pafe-------------------------------------------")
            
        
            if case_type not in ['FIREWALL','MES','OTHER','firewall','mes','other']:
                print("===============================================================")
                return jsonify({'message': 'Bad Request', 'error': True}), 400
            
            conn = init()
            print("hello2")

            if conn is None:
                return jsonify({'message': 'Database connection failed', 'error': True}), 500
            
            if page:
                output,total_count, status_code = cases_list.cases_list_pagination(conn,case_type,alert_type,page)
                print(output,"my output---------------------------------------")

                if status_code != 200:
                    return jsonify({"error":True, "data":output}), status_code
            
                return jsonify({"error":False, "data":output,"total_pages":total_count}), status_code


            output, status_code = cases_list.cases_list(conn,case_type,alert_type)
            print("hello3")

            if status_code != 200:
                return jsonify({"error":True, "data":output}), status_code
            
            return jsonify({"error":False, "data":output}), status_code
        
        except Exception as e:
            logging.error(str(e))
            print("*********************")
            return jsonify({
                'message': 'Internal server error',
                'error': True,
            }), 500
    else:
        return jsonify({
            'message': '405 Method Not Allowed',
            'error': True,
        }), 405
