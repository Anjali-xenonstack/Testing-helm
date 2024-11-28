from .dbConfig import db_params
import psycopg2
import logging

db_config = db_params
logging.basicConfig(level=logging.INFO)
Please_enter_a_ValidParams_MSG = 'Please enter valid parameters'
Database_conn_None = 'Database connection is None.'
Internal_server_error = 'Internal Server Error'


def connect_to_db():
    try:
        conn = psycopg2.connect(**db_config)
        logging.info("Database connection established successfully!")
        return conn
    except psycopg2.Error as e:
        logging.error(f"Error connecting to the database: {str(e)}")
        return None
    

def check_db_connection():
    conn = connect_to_db()
    if conn is not None:
        return True
    else:
        return False


def perform_query(conn, query, params=None):
    logging.info("perform_query_executes")
    try:
        if conn is not None:
            if params != " ":
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchall()
                    conn.commit()
                    logging.info(result)
                    logging.info(params)
                    if result is not None:
                        return {'result': result, 'error': False}, 200
                    else:
                        return {'result': result, 'error': True}, 404
            else:
                return {
                    'message': Please_enter_a_ValidParams_MSG,
                    'error': True
                }, 400

        else:
            logging.error(Database_conn_None)
            return {
                'message': Internal_server_error,
                'error': True
            }, 500
    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"Error executing query: {str(e)}")
        return {
            'message': f"Error executing query: {str(e)}",
            'error': True
        }, 500


def perform_query_post(conn, query, params=None):
    logging.info("perform_query_executes")
    try:
        if conn is not None:
            if params is not None:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchone()
                    column_names = [desc[0] for desc in cursor.description]
                    conn.commit()
                    logging.info(result)
                    logging.info(params)
                    if result is not None:
                        result_dict = dict(zip(column_names, result))
                        return result_dict
                    else:
                        return {'result': result, 'error': True}, 404
            else:
                return {
                    'message': Please_enter_a_ValidParams_MSG,
                    'error': True
                }, 400

        else:
            logging.error(Database_conn_None)
            return {
                'message': Internal_server_error,
                'error': True
            }, 500
    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"Error executing query: {str(e)}")
        return {
            'message': f"Error executing query: {str(e)}",
            'error': True
        }, 500


def perform_query_put(conn, query, params=None):
    logging.info("perform_query_executes")
    try:
        if conn is not None:
            if params is not None:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    logging.info(params)
                    # Check if any rows were affected by the update
                    if cursor.rowcount >0:
                        return {'result': 'Update successful', 'error': False}, 200
                    else:
                        return {'result': 'No rows updated', 'error': True}, 404
            else:
                return {
                    'message': Please_enter_a_ValidParams_MSG,
                    'error': True
                }, 400
        else:
            logging.error(Database_conn_None)
            return {
                'message': Internal_server_error,
                'error': True
            }, 500
    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"Error executing query: {str(e)}")
        return {
            'message': f"Error executing query: {str(e)}",
            'error': True
        }, 500
