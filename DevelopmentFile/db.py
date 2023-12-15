import psycopg2
import psycopg2.extras
from config import config

def connect():
  try : 
    conn=None
    params=config()
    print('Connection à la base de donnée postgreSQL ...')
    conn=psycopg2.connect(**params)
    print(conn.encoding)
    conn.set_client_encoding("UNICODE")
    cur = conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)

    print(conn.encoding)
    #create cursor 
    crsr=conn.cursor()
    crsr.execute('SELECT version()')
    db_version=crsr.fetchone()
    print(db_version)
    return conn
  except(Exception,psycopg2.DatabaseError) as error:
    print(error)


if __name__=="__main__":
  connect()