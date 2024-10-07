#!/bin/bash

set -e

echo "Initializing PostgreSQL database from Compose ..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

    -- Create a new user
    CREATE USER "$POSTGRES_APP_USER" WITH PASSWORD '$POSTGRES_APP_PASSWORD';

    -- Create a new database
    CREATE DATABASE "$DB_NAME";

    -- Grant privileges on public
    GRANT ALL PRIVILEGES ON DATABASE "$DB_NAME" TO "$POSTGRES_APP_USER";

    -- Check available databases
    SELECT datname FROM pg_database;

EOSQL

echo "PostgreSQL initialization completed."


# TODO: to fix and use with Postgres 16.4
# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
#     -- Create a new user
#     CREATE USER "$DB_USER" WITH PASSWORD '$DB_PASSWORD';

#     -- Create a new database
#     CREATE DATABASE "$DB_NAME";

#     -- Grant privileges on public
#     GRANT ALL PRIVILEGES ON DATABASE "$DB_NAME" TO "$DB_USER";

#     -- WIP

#     -- Create a schema for the user
#     -- CREATE SCHEMA IF NOT EXISTS "${DB_USER}_schema" AUTHORIZATION "$DB_USER";

#     -- Grant all privileges on the schema to the user
#     -- GRANT ALL ON SCHEMA "${DB_USER}_schema" TO "$DB_USER";

#     -- Grant usage and creation privileges on the schema
#     -- GRANT USAGE, CREATE ON SCHEMA "${DB_USER}_schema" TO "$DB_USER";

#     -- Grant privileges on the schema to the user
#     -- GRANT ALL PRIVILEGES ON SCHEMA "${DB_USER}_schema" TO "$DB_USER";
#     -- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "${DB_USER}_schema" TO "$DB_USER";
#     -- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA "${DB_USER}_schema" TO "$DB_USER";

#     -- Optionally, set the search path to this schema (so it's used by default)
#     -- ALTER ROLE "$DB_USER" SET search_path TO "${DB_USER}_schema", public;

#     -- Optionally, drop the default postgres database
#     -- DROP DATABASE IF EXISTS "postgres";

#     -- Check available databases
#     SELECT datname FROM pg_database;

#     -- Check schema privileges
#     SELECT nspname, usename, has_schema_privilege(usename, nspname, 'USAGE')
#     FROM pg_namespace
#     CROSS JOIN pg_user
#     WHERE nspname = '${DB_USER}_schema';

#     -- more checks
#     SELECT * FROM information_schema.role_table_grants WHERE grantee = '$DB_USER';

# EOSQL

# echo "PostgreSQL database initialized successfully."


# DRAFTS
# -- Grant specific usage and create privileges on the public schema
# GRANT USAGE, CREATE ON SCHEMA public TO "$DB_USER";

# -- Optionally, transfer ownership of the public schema to the user
# ALTER SCHEMA public OWNER TO "$DB_USER";

# ALTER USER "$DB_USER" WITH SUPERUSER;
