import os
import random
import redis
from typing import List, Union, Tuple, ByteString, Dict
import json
from dotenv import load_dotenv
import logging


logger = logging.getLogger(__package__)


def generate_random_id(max_num: int) -> int:
    """
    This function generates random id num until max_num
    """
    return random.randint(0, max_num)


def generate_random_ipv4() -> str:
    """
    This function generates random ipv4 (format: 10.233.111.22)
    """
    ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    return ip


def generate_random_mac() -> str:
    """
    This function generates random mac address (format: 22:4F:2A:15:BC)
    """
    mac = ':'.join([hex(random.randint(0, 255))[2:].upper() for _ in range(6)])
    return mac


load_dotenv()


START_RECORDS = (
    {'id': generate_random_id(1000), 'ip': '10.12.11.1', 'mac': 'af:sc:sa:fs:00:01'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.2', 'mac': 'af:sc:sa:fs:00:02'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.3', 'mac': 'af:sc:sa:fs:00:03'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.4', 'mac': 'af:sc:sa:fs:00:04'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.5', 'mac': 'af:sc:sa:fs:00:05'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.6', 'mac': 'af:sc:sa:fs:00:06'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.7', 'mac': 'af:sc:sa:fs:00:07'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.8', 'mac': 'af:sc:sa:fs:00:08'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.9', 'mac': 'af:sc:sa:fs:00:09'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.10', 'mac': 'af:sc:sa:fs:00:10'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.11', 'mac': 'af:sc:sa:fs:00:11'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.12', 'mac': 'af:sc:sa:fs:00:12'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.13', 'mac': 'af:sc:sa:fs:00:13'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.14', 'mac': 'af:sc:sa:fs:00:14'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.15', 'mac': 'af:sc:sa:fs:00:15'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.16', 'mac': 'af:sc:sa:fs:00:16'},
    {'id': generate_random_id(1000), 'ip': '10.12.11.17', 'mac': 'af:sc:sa:fs:00:17'},
)


class RedisManager:
    def __init__(self):
        self._connection = None
        self.redis_queue_name = os.getenv('REDIS_QUEUE_NAME')

    @property
    def connection(self):
        if self._connection is None:
            self._connection = redis.Redis(host=os.getenv('REDIS_CONNECTION_HOST', '127.0.0.1'),
                                           port=os.getenv('REDIS_CONNECTION_PORT', 6379),
                                           db=0)
        return self._connection

    def check_redis_queue_length(self):
        return self.connection.llen(self.redis_queue_name)

    def get_record_from_queue(self):
        #TODO: change naming flag
        flag = True
        valid_record = None
        while self.check_redis_queue_length() and flag:
            flag = False
            raw_record = self.connection.rpop(self.redis_queue_name)
            valid_record = self.get_valid_data(raw_record)
            if valid_record is None:
                flag = True

        return valid_record

    @staticmethod
    def get_valid_data(raw_record: ByteString):
        valid_data = None
        try:
            valid_data = json.loads(raw_record.decode())
        except (json.JSONDecodeError, AttributeError) as err:
            logger.warning(f'Record is not json serializable {err} and will be deleted from queue.')

        return valid_data

    def add_record_to_queue(self, record: Dict):
        raw_record = json.dumps(record)
        self.connection.lpush(self.redis_queue_name, raw_record)


# redis1 = RedisManager()
# redis1.add_record_to_queue({'id': 1, 'ip': '1'})
# print(redis1.get_records_from_queue()[0])
# redis1.add_record_to_queue({'id': 1, 'ip': '10.12.11.7', 'mac': 'af:sc:sa:fs:00:07'})
# redis1.add_record_to_queue({'id': generate_random_id(1000), 'ip': '10.12.11.7', 'mac': 'af:sc:sa:fs:00:07'})
# redis1.add_record_to_queue({'id': generate_random_id(1000), 'ip': '10.12.11.7', 'mac': 'af:sc:sa:fs:00:07'})
# redis1.add_record_to_queue({'id': generate_random_id(1000), 'ip': '10.12.11.7', 'mac': 'af:sc:sa:fs:00:07'})
# redis1.add_record_to_queue({'id': generate_random_id(1000), 'ip': '10.12.11.7', 'mac': 'af:sc:sa:fs:00:07'})
# print(redis1.get_records_from_queue()[0])
# print(redis1.get_record_from_queue())
