import os
import infi.clickhouse_orm
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Database:
    """
    Database instances connect to a specific ClickHouse database for running queries,
    inserting data and other operations.
    """

    def __init__(self, db_name,
                 db_url=os.getenv('DB_URL'),
                 username=None, password=None, readonly=False, autocreate=True,
                 timeout=60):
        self.db_name = db_name
        self.db_url = db_url


# import os
# from dotenv import load_dotenv
# from infi.clickhouse_orm import Database
#
#
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
#
#
# def db_connect():
#     db = Database('my_test_db')
#     db = Database(
#         os.getenv('DB_NAME'),
#         db_url=os.getenv('DB_URL'),
#         username=os.getenv('USERNAME'),
#         password=os.getenv('PASSWORD')
#     )

# if __n
#     Проверить очередь
