import logging
import os
import sys
import jwt
from utils import database_connection, decode_andfetch_user_id
from signup.queries import queries
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


def signup_func(conn, email, username, password):
    try:
        cursor = conn.cursor()
        Check_user_query = queries.Check_user_query.rstrip("\n")
        cursor.execute(Check_user_query, (email,))
        result = cursor.fetchall()
        if not result:
            print("email",email, "password", password, "username: ", username)
            cursor.execute(queries.signup_query, (email, password, username))  
            if cursor.rowcount > 0:
                conn.commit()
                return {"message": "User registered successfully", "error": False}, 200
            else:
                return {"message": "Internal server error", "error": True}, 500
        else:
            return {"message": "User is already registered", "error": True}, 400

    except Exception as e:
        logging.error(f"Error in signup function: {str(e)}", exc_info=True)
        return {
            'message': f'Internal server error: {str(e)}',
            'error': True
        }, 500
