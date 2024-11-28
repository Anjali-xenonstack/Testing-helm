import logging
import os
import sys
import time
import jwt
from utils import database_connection, decode_andfetch_user_id
from logout.queries import queries
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


def logout_func(conn, token, email):
    try:
        cursor = conn.cursor()
        cursor.execute(queries.Check_token_query, (token,))
        result = cursor.fetchone()
        if result:
            return {"message": "User is already logged out", "error": False}, 200
        cursor.execute(queries.Logout_query, (token,))
        if cursor.rowcount > 0:
            conn.commit()
            return {"message": "Logged out successfully", "error": False}, 200
        else:
            return {"message": "Internal server error", "error": True}, 500
    except Exception as e:
        logging.error(f"Error in logout function: {str(e)}", exc_info=True)
        return {
            'message': f'Internal server error: {str(e)}',
            'error': True
        }, 500

