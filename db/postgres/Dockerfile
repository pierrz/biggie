FROM postgres:14.9

# TODO: enable file logging (issue with permissions, root always coming back)
# USER root
# COPY ./postgresql.conf /etc/postgresql/postgresql.conf
# RUN mkdir -p /var/log/postgres && \
#     touch /var/log/postgres/postgresql.log && \
#     chown -R postgres:postgres /var/log/postgres && \
#     chmod 755 -R /var/log/postgres \
#     && chown postgres:postgres /etc/postgresql/postgresql.conf

# USER postgres
# CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]


# TODO: implement v16.4
# issues with creating tables (permission denied for schema public)
# FROM postgres:16.4
# COPY ./pg_hba.conf /etc/postgresql/pg_hba.conf

# CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
