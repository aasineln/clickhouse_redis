from redis_queue.redis_queue import RedisManager
from process_record import process_record


def main():
    redis = RedisManager()

    record = redis.get_record_from_queue()
    while record:
        process_record(record, redis)
        record = redis.get_record_from_queue()


if __name__ == '__main__':
    main()
