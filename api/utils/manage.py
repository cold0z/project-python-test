import os
from flask import jsonify
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(host='db',
        database=os.environ.get('POSTGRES_DB'),
        user= os.environ.get('POSTGRES_USER'),
        port=os.environ.get('POSTGRES_PORT'),
        password=os.environ.get('POSTGRES_PASSWORD'))
    return conn


def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    email character varying COLLATE pg_catalog."default",
    password character varying(255) COLLATE pg_catalog."default",
    registration_date character varying(255) COLLATE pg_catalog."default",
    active boolean,
    code character varying(8) COLLATE pg_catalog."default",
    code_date character varying(100) COLLATE pg_catalog."default",
    confirmed boolean,
    confirmed_on character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (id)
)
   """)
    conn.commit() 
    cur.close()
    conn.close()
    print("data table added")


def insert_test_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
   INSERT INTO users(
	email, password, registration_date, active, code, code_date)
	VALUES ('webenfly@gmail.com', '3cbbbba6c8045bb006e27f2c6249c2ea', '2022-04-22', false, '123456', '2022-04-22 14:52:46.56793')
    """)
    conn.commit() 
    cur.close()
    conn.close()
    print("data test inserted")


if __name__ == "__main__":
    create_table()
    insert_test_data()