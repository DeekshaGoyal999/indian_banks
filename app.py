from flask import Flask, request, Blueprint, jsonify, Response
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, JWT_SECRET_KEY
from flask_mysqldb import MySQL
import os
import jwt
from hashlib import pbkdf2_hmac
from functools import wraps
import datetime

app = Flask(__name__)

authentication = Blueprint("authentication", __name__)

app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

db = MySQL(app)


def db_read(query, params=None):
    cursor = db.connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    entries = cursor.fetchall()
    cursor.close()

    content = []

    for entry in entries:
        content.append(entry)

    return content


def db_write(query, params):
    cursor = db.connection.cursor()
    try:
        cursor.execute(query, params)
        db.connection.commit()
        cursor.close()

        return True

    except MySQL._exceptions.IntegrityError:
        cursor.close()
        return False


def generate_salt():
    salt = os.urandom(16)
    return salt.hex()


def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()


def generate_jwt_token(content):
    # token = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    
    # return token
    
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    token = str(encoded_content).split("'")
    return token[1]


def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False


def validate_user(email, password):
    current_user = db_read("""SELECT * FROM users WHERE email = %s""", (email,))

    if len(current_user) == 1:
        saved_password_hash = current_user[0]["password_hash"]
        saved_password_salt = current_user[0]["password_salt"]
        password_hash = generate_hash(password, saved_password_salt)
        if password_hash == saved_password_hash:
            user_id = current_user[0]["email"]
            jwt_token = generate_jwt_token({"email": user_id, "exp": datetime.datetime.now()+ datetime.timedelta(days=5)})
            return jwt_token
        else:
            return False

    else:
        return False

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
           current_user = data['email']
       except:
           return jsonify({'message': 'token is invalid'})
       return f(current_user, *args, **kwargs)
   return decorator


@app.route('/ifsc/<string:ifsc_code>')
@token_required
def ifsc_get(current_user,ifsc_code):
    limit = request.args.get('limit', default = 100, type = int)
    offset = request.args.get('offset', default = 0, type = int)
    conn = db.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM banks_branches where ifsc=%(ifsc)s LIMIT %(limit)s OFFSET %(offset)s;", { 'ifsc': ifsc_code, 'limit': limit, 'offset': offset })
    branch_details = cur.fetchall()
    conn.commit()
    return jsonify({'branch_details': branch_details})

@app.route('/bank_name/<string:bank_name>/city/<string:city>')
@token_required
def branch_city_get(current_user, bank_name,city):
    limit = request.args.get('limit', default = 100, type = int)
    offset = request.args.get('offset', default = 0, type = int)
    conn = db.connection
    cur =  conn.cursor()
    cur.execute("SELECT * FROM banks_branches where bank_name=%(name)s and city=%(city)s LIMIT %(limit)s OFFSET %(offset)s;", {'name': bank_name, 'city': city, 'limit': limit, 'offset': offset})
    branches = cur.fetchall()
    conn.commit()
    return jsonify({'branch_details': branches})

@authentication.route("/register", methods=["POST"])
def register_user():
    user_email = request.json["email"]
    user_password = request.json["password"]
    user_confirm_password = request.json["confirm_password"]

    if user_password == user_confirm_password and validate_user_input(
        "authentication", email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)

        if db_write(
            """INSERT INTO users (email, password_salt, password_hash) VALUES (%s, %s, %s)""",
            (user_email, password_salt, password_hash),
        ):
            return Response(status=201)
        else:
            return Response(status=409)
    else:
        return Response(status=400)

# Function to login a valid user
@authentication.route("/login", methods=["POST"])
def login_user():
    user_email = request.json["email"]
    user_password = request.json["password"]

    user_token = validate_user(user_email, user_password)
    print(user_token)
    if user_token:
        return jsonify({"jwt_token": user_token})
    else:
        return Response(status=401)
 

app.register_blueprint(authentication, url_prefix="/api/auth")

app.run(host='localhost', port=5000, debug=True)

