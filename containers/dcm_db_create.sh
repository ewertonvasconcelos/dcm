#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER dcm;
    ALTER USER dcm WITH PASSWORD 'password';
    CREATE DATABASE dcm;
    GRANT ALL PRIVILEGES ON DATABASE dcm TO dcm;
EOSQL