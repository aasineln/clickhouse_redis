clickhouse-client --query "CREATE DATABASE IF NOT EXISTS db_users"

clickhouse-client --query "CREATE TABLE IF NOT EXISTS db_users.profile
(
    username String,
    ipv4 IPv4,
    mac String
)
ENGINE = MergeTree()
ORDER BY username;"

clickhouse-client --format_csv_delimiter=";" --query="INSERT INTO db_users.profile FORMAT CSV" < upload_data_to_db.csv