import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect("postgresql://postgres:shaikh123@localhost:5432/postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    try:
        cur.execute("CREATE DATABASE awsservers;")
        print("Database 'awsservers' created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print("Database 'awsservers' already exists.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error connecting to Postgres: {e}")
