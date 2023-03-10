import os
import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("CS_USER")
password = os.getenv("CS_PASS")
dbName = "p320_34"


try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('localhost', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'database': dbName,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }


        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")
        conn.close()
except:
    print("Connection failed")