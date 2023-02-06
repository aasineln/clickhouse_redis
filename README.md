#  Сервис поиска учетной записи с последующей отправкой во внешний сервис
1) БД CLickhouse c таблицей, содержащей поля: username, ipv4, mac
2) Redis работает с очередью задач. Объект очереди имеет поля: id, ipv4, mac
3) Сервис осуществляет поиск username по полям ipv4 и mac. В случае успеха отправляет результирующий JSON во внешний сервис (например, https://pastebin.com)
4) Сервис сохраняет url, полученный от внешнего ресурса в файл
____
## Запуск приложения
1. Скопируйте все файлы проекта в отдельную дерикторию и установите библиотеки из requirements.txt
2. **ClickHouse** может работать на любой операционной системе Linux, FreeBSD или Mac OS X с архитектурой процессора x86_64, AArch64 или PowerPC64LE. Предварительно собранные пакеты компилируются для x86_64 и используют набор инструкций SSE 4.2, поэтому, если не указано иное, его поддержка в используемом процессоре, становится дополнительным требованием к системе. Вот команда, чтобы проверить, поддерживает ли текущий процессор SSE 4.2:
```bash
$ grep -q sse4_2 /proc/cpuinfo && echo "SSE 4.2 supported" || echo "SSE 4.2 not supported"
```
Для установки ClickHouse из DEB пакетов выполните:
```bash
$ sudo apt-get install -y apt-transport-https ca-certificates dirmngr
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754
$ echo "deb https://packages.clickhouse.com/deb stable main" | sudo tee \
    /etc/apt/sources.list.d/clickhouse.list
$ sudo apt-get update
$ sudo apt-get install -y clickhouse-server clickhouse-client
$ sudo service clickhouse-server start
```
Без установки. Запуск БД Clickhouse в контейнере из Docker образа:
```bash
$ docker run -d --name my-clickhouse-server -p 9000:9000 --ulimit nofile=262144:262144 clickhouse/clickhouse-server
```
Чтобы заполнить БД данными из CSV файла, копируем файл upload_data_to_db.csv в контейнер и подключаемся к контейнеру:
```bash
$ docker cp upload_data_to_db.csv my-clickhouse-server:/upload_data_to_db.csv
$ docker exec -it my-clickhouse-server /bin/bash
$ clickhouse-client --format_csv_delimiter=";" --query="INSERT INTO db_users.profile FORMAT CSV" < upload_data_to_db.csv
```
3. **Redis** - https://redis.io/docs/getting-started/installation/install-redis-on-linux/  
Без установки. Запуск в Docker контейнере: 
```bash
$ docker run -p 6379:6379 -it redis/redis-stack:latest
```
Работа с Redis:
```bash
$ docker exec -it some-redis redis-cli (клиент командной строки)
$ docker exec -it some-redis /bin/bash
```
4. Отправка данных во внешний сервис (https://pastebin.com) и получение ссылки.  
  Необходимо зарегистрироваться https://pastebin.com/ и получить API_KEY.
____
## Requirements.txt  
  python-dotenv==0.21.1  
  requests==2.28.2  
  redis==4.4.2  
  clickhouse-driver==0.2.5  
