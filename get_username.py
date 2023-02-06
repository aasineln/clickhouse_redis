class ClickhouseManager:
    def __init__(self):
        self._connection = None
        self.clickhouse_db_name = os.getenv('REDIS_QUEUE_NAME')

    @property
    def connection(self):
        if self._connection is None:
            self._connection = redis.Redis(host=os.getenv('REDIS_CONNECTION_HOST', '127.0.0.1'),
                                           port=os.getenv('REDIS_CONNECTION_PORT', 6379),
                                           db=0)


# from infi.clickhouse_orm import Database
#
#
# db = Database('db_users', db_url='http://127.0.0.1:8123', username='default', password='')

from clickhouse_driver import Client
client = Client(host='127.0.0.1',
                port=9000,
                user='default',
                password='',
                database='system',
                secure=False)
client.get_connection()
print(client.execute('SHOW DATABASES'))

# from clickhouse_driver import Client, connect
# from clickhouse_driver import connect
#
#
# conn = connect('clickhouse://127.0.0.1:8123')
# cursor = conn.cursor()
# cursor.execute('SHOW TABLES')
# client = Client.from_url('clickhouse://default@127.0.0.1:8123/system')

# client.execute('SHOW TABLES')

# result: status (successful, failure), username ('dimas', None), mac, ip, status info
#
# 1. Exception БД недоступна, InternalSeverFailure
# что делать? К БД 3 попытки (переменная)
#
# 2. failure. БД доступна, нет username, UserNotFound -> log.info
# отправка на pastebin
# получаем ссылку
# удаляем запись в очереди
#
# 3. successful. В БД всё есть -> username, ip, mac
# отправка на pastebin
# получаем ссылку
# удаляем запись в очереди


# if username_info['status_code'] == ERROR_DB_CONNECTION:
#     attempt_count += 1
#     continue