FROM postgres:14.9

COPY ./docker-entrypoint-initdb.d/init-postgres.sh /docker-entrypoint-initdb.d/init-postgres.sh

# TODO: implement v16.4
# issues with creating tables (permission denied for schema public)
# FROM postgres:16.4

# COPY ./pg_hba.conf /etc/postgresql/pg_hba.conf

# CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
