FROM mongo:7.0.14

# Cf. https://www.mongodb.com/docs/manual/reference/configuration-options/#systemlog-options
# enable file logging
# USER root
# RUN mkdir -p /var/log/mongodb \
#     && chown -R mongodb:mongodb /var/log/mongodb

USER mongodb
CMD ["-f", "/etc/mongod.conf"]