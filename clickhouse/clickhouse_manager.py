import os
from clickhouse_driver import Client
from csv import DictReader
from dotenv import load_dotenv
import logging


load_dotenv()
logger = logging.getLogger(__package__)


class ClickhouseManager:
    def __init__(self, db_name='default'):
        self._connection = None
        self.db_name = db_name

    @property
    def connection(self):
        if self._connection is None:
            self._connection = Client(host='localhost', port=9000)
        return self._connection

    def create_db(self):
        self.connection.execute('CREATE DATABASE IF NOT EXISTS `%s`' % self.db_name)

    def drop_db(self, db_name):
        self.connection.execute('DROP DATABASE IF EXISTS `%s`' % db_name)

    def create_table(self, db_name, table_name):
        self.connection.execute('CREATE TABLE IF NOT EXISTS `%s`.`%s` (username String, ipv4 String, mac String) ENGINE = MergeTree() ORDER BY username;' % (db_name, table_name))

    def drop_table(self, db_name, table_name):
        self.connection.execute('DROP TABLE IF EXISTS `%s`' % table_name)

    # @staticmethod
    # def iter_csv(filename):
    #     converters = {
    #         'username': str,
    #         'ip': str,
    #         'mac': str
    #     }
    #
    #     with open(filename, 'r') as f:
    #         for line in f.readlines():
    #             print(line.strip())
                # print({k: v for k, v in line.items()})

    def fill_table_from_csv(self, db_name, table_name, csv_path):
        # self.connection.execute_iter("INSERT INTO %s.%s FROM INFILE '%s' FORMAT CSV;" % (db_name, table_name, csv_path))
        self.connection.execute("INSERT INTO profile_db.profile_table FROM INFILE '../upload_data_to_db.csv' FORMAT CSV;")

    def get_record_from_table(self, db_name, table_name):
        print("SELECT * FROM %s.%s" % (db_name, table_name))
        self.connection.execute("SELECT * FROM %s.%s" % (db_name, table_name))


cl = ClickhouseManager()
# cl.create_db()
# print(cl.create_table('profile_db', 'profile_table'))
# print(cl.fill_table_from_csv('profile_db', 'profile_table', '../upload_data_to_db.csv'))
print(cl.get_record_from_table('db_users', 'profile'))

# cl.connection.execute('select * from db_users.profile')
# cl.connection.execute("select * from db_users.profile where username='user201'")

