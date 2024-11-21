#!/bin/bash
set -e

psql -U postgres <<-EOSQL
    CREATE DATABASE django;
    CREATE USER postgres WITH PASSWORD felipe;
    GRANT ALL PRIVILEGES ON DATABASE django TO postgres;
EOSQL
