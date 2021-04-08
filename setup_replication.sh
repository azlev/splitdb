#!/bin/bash

set -xe


docker-compose exec web ./manage.py migrate
docker-compose exec web ./manage.py migrate --database integration

PGPASSWORD=postgres

psql -h 127.0.0.1 -p 5433 -U postgres integration <<EOSQL
ALTER SYSTEM SET wal_level = 'logical';
CREATE PUBLICATION lw_integration FOR TABLE integration_son ;
INSERT INTO integration_son (father_id) (SELECT generate_series(10001, 20000));
EOSQL

psql -h 127.0.0.1 -p 5432 -U postgres loggi <<EOSQL
ALTER SYSTEM SET wal_level = 'logical';
CREATE TABLE integration_son (id int PRIMARY KEY, father_id int);
CREATE SUBSCRIPTION lw_integration CONNECTION 'host=integration user=postgres password=postgres dbname=integration' PUBLICATION lw_integration;
SELECT pg_sleep(10);
INSERT INTO loggi_father (SELECT father_id FROM integration_son);
SELECT setval('loggi_father_id_seq', father_id) FROM integration_son ORDER BY id DESC LIMIT 1;
EOSQL

