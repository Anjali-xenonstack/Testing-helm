from itsdangerous import URLSafeSerializer
import os ,sys
import time
import logging
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import database_connection  # noqa

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




def generate_jwt_token(email):
    try:
        secret_key = os.environ.get("JWT_SECRET_KEY", "testing")
        serializer = URLSafeSerializer(secret_key)
        expiration = int(time.time()) + 3600 
        payload = {"email": email}
        payload['exp'] = expiration
        token = serializer.dumps(payload)

        return token
    except Exception as e:
        print("Error generating JWT token:", str(e))
        return None



def decode_jwt_token(token):
    try:
        secret_key = os.environ.get("JWT_SECRET_KEY", "testing")
        serializer = URLSafeSerializer(secret_key)
        payload = serializer.loads(token)
        if 'exp' in payload:
            expiration_time = payload['exp']
            current_time = int(time.time())
            if current_time > expiration_time:
                print("Token has expired")
                return "Token has expired" ,401
        print("hello7")
        print("email extracted from token", payload['email'])
        print(payload['email'])
        return "" ,200
    except Exception as e:
        print("Error decoding JWT token:", str(e))
        return "Error decoding token" ,401
    
    
    
def get_userId(conn, email):
    if email is None or email == "":
        return "Email is Empty" , 400
    try:
        cursor = conn.cursor()
        query = "select _id from public.user where email = %s"
        cursor.execute(query, (email, ))
        email_result = cursor.fetchall()
        if email_result:
            return email_result[0][0], 200
        else:
            return "user for that email is not exist" , 404      
    except Exception as e:
        print("error reason", e)
        return "Internal Server error", 500
    
    