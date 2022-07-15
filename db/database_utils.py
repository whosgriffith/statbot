import os
from dotenv import load_dotenv
import psycopg2
from loguru import logger

load_dotenv()
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')


def db_connect_and_cursor():
    con = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
    cur = con.cursor()
    return con, cur


def active_sessions_cleanup():
    logger.info("Initiating session cleanup.")
    try:
        con, cur = db_connect_and_cursor()
        query = "DELETE FROM user_voice_sessions WHERE left_at IS null"
        cur.execute(query)
        con.commit()
        con.close()
        logger.success("Active session cleanup done.")
        logger.info(f"Deleted {cur.rowcount} active sessions.")
    except Exception as ex:
        logger.exception("An error occurred while cleaning active sessions:")
        print(ex)
