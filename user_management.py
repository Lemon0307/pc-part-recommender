from flask import request, jsonify, Blueprint, session
from bcrypt import hashpw, gensalt
from db import get_driver
import datetime
import uuid
import jwt

user_management = Blueprint('user_management', __name__)

# change in final version
SECRET_KEY = "verysecretkey"

def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return "invalid"

@user_management.route('/login', methods=['POST'])
def login():
    driver = get_driver()
    
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    # retrieve user
    get_user_query = "MATCH (u:User {username: $username}) RETURN u.password AS password"
    result = driver.execute_query(get_user_query, username=username)
    
    if not result.records:
        return jsonify({"error": "Invalid username"}), 401
    
    stored_password_hash = result.records[0]["password"]
    
    # verify password
    if not hashpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')) == stored_password_hash.encode('utf-8'):
        return jsonify({"error": "Invalid password"}), 401
    
    # generate JWT token
    token = jwt.encode({"username": username, 
                        "password": password}, 
                        SECRET_KEY, algorithm="HS256")
    
    print(type(token), token)
    
    print(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=720))

    return jsonify({"message": "Login successful", "token": token}), 200

@user_management.route('/sign_up', methods=['POST'])
def sign_up():
    driver = get_driver()
    
    data = request.json
    username = data.get("username")
    password = data.get("password")
    password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
    print(password_hash)
    
    # check if user already exists
    check_user_query = "MATCH (u:User {username: $username}) RETURN u"
    result = driver.execute_query(check_user_query, username=username)
    
    if result.records:
        return jsonify({"error": "Username already exists"}), 400
    
    properties = data
    properties["password"] = password_hash
    properties["user_id"] = str(uuid.uuid4())
    # Create new user
    create_user_query = "CREATE (u:User $props) RETURN u.user_id"
    
    result = driver.execute_query(create_user_query, props=properties)
    
    return jsonify({"user_id": "Successfully created user"}), 201