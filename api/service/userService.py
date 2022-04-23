from calendar import c
from datetime import datetime
import os

from flask import jsonify
from api.constants import SALT
from api.model.user import User
import hashlib
import psycopg2


def get_db_connection():
    conn = psycopg2.connect(host='db',
        database=os.environ.get('POSTGRES_DB'),
        user= os.environ.get('POSTGRES_USER'),
        port=os.environ.get('POSTGRES_PORT'),
        password=os.environ.get('POSTGRES_PASSWORD'))
    return conn


def check_user(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = TRIM(%s)", [email])
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def insert_user(user = User):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO USERS (email,password,registration_date, active, code, code_date) values (%s,%s,%s,%s,%s,%s)  ", [user.email,user.password,user.registration_date, user.active, user.code, user.code_date])
        conn.commit() 
        cur.close()
        conn.close()
        return True
    except Exception as inst:
        print("inst",inst)
        return False    




def verify_auth(email,password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = TRIM(%s) and password = TRIM(%s)", [email,password])
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data


def verify_user(email):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE USERS set active = true WHERE email =%s ", [email])
        conn.commit() 
        cur.close()
        conn.close()
        return True
    except Exception as inst:
        print("inst",inst)
        return False    



def hash_password(password):
    salt = SALT
    password_salted = password+salt
    password_hashed = hashlib.md5(password_salted.encode())
    return password_hashed.hexdigest()
    


def register_user(email,
                    password):

    today_date = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now()
    code = "123456"
    new_user = User(email.lower(), hash_password(password.strip()), today_date, 
    False,code,now)
    if insert_user(new_user):
        return new_user


