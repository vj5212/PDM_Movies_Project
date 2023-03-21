import os
import traceback
import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("CS_USER")
password = os.getenv("CS_PASS")
dbName = "p320_34"

def execute_query_one(exe_string, data):
    try:
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('localhost', 5432)) as server:
            server.start()
            params = {
                'database': dbName,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
            }


            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            curs.execute(exe_string, data)
            return curs.fetchone()
    except Exception as e:
        print("Connection failed")
        print(e)
        traceback.print_exc()
    finally:
        conn.close()


def execute_query_all(exe_string, data):
    try:
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('localhost', 5432)) as server:
            server.start()
            params = {
                'database': dbName,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
            }

            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            curs.execute(exe_string, data)
            return curs.fetchall()
    except Exception as e:
        print("Connection failed")
        print(e)
        traceback.print_exc()
    finally:
        conn.close()
