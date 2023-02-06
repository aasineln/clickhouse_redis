import os
import logging
from typing import Dict, Optional
from redis_queue.redis_queue import RedisManager

DEFAULT_ATTEMPT_COUNT = 3
logger = logging.getLogger(__package__)


def process_record(record: Dict, redis: RedisManager) -> None:
    valid_record = get_valid_record(record)

    if valid_record is None:
        logger.warning(f'Invalid format record: {record}')
        return

    # attempt_count = 0
    # while attempt_count < os.getenv('RETRY_ATTEMPT_COUNT', DEFAULT_ATTEMPT_COUNT):
    username_info = get_username(valid_record)


    url_result = send_result(username_info)

    # if url_result is None:
    #     attempt_count += 1
    #     continue
    #
    writing_status = write_result(url_result)
    if writing_status == ERROR_WRITNIG_STATUS:
        redis.add_record_to_queue(record)
        return


def get_valid_record(record: Dict) -> Optional[Dict]:
    #TODO: logger
    if not isinstance(record, dict):
        return
    mandatory_fields = ['id', 'ip', 'mac']

    for mandatory_field in mandatory_fields:
        if mandatory_field not in record:
            return

    return record
