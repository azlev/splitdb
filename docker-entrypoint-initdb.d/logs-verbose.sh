#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    ALTER SYSTEM SET log_min_messages = 'error';
    ALTER SYSTEM SET log_min_error_statement = 'log';
    ALTER SYSTEM SET log_statement = 'all';
    ALTER SYSTEM SET log_line_prefix = '%m [%p] %q[user=%u,db=%d,app=%a] ';
    ALTER SYSTEM SET log_checkpoints = on;
    ALTER SYSTEM SET log_connections = on;
    ALTER SYSTEM SET log_disconnections = on;
    ALTER SYSTEM SET log_lock_waits = on;
EOSQL

