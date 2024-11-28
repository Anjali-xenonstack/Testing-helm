import logging
import os
import sys
from utils import  decode_andfetch_user_id
from login.queries import queries
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(parent_dir)


def login_func(conn,email, password):
    try:
        cursor = conn.cursor()
        query = queries.Login_query_check_userid.rstrip("\n")
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        print(user)
        if user is None:
            return {"message":"user not exist","error":True}, 401
        
        _, db_password = user
        if db_password != password:
            return {"message": "Incorrect password", "error": True}, 401
        token = decode_andfetch_user_id.generate_jwt_token(email)
        print("token", token)
        if token is None:
            return {"message":"Internal server error(token generation part)","error":True}, 500
        # another_cursor = conn.cursor()
        # another_cursor.execute(queries.Enter_into_Session_log_query, (user_id,user_id,token))
        conn.commit()
        return {
            "token": token,
            "error": False
        }, 200
    except Exception as e:
        logging.error(str(e), exc_info=True)
        return {
            'message':"Internal Server Error" ,
            'error': True
        }, 500
    finally:
        cursor.close()
