FROM mongo:7.0.14

# TODO: enable file logging
# Cf. https://www.mongodb.com/docs/manual/reference/configuration-options/#systemlog-options
# USER root
# RUN mkdir -p /var/log/mongodb \
#     && chown -R mongodb:mongodb /var/log/mongodb

USER mongodb
CMD ["-f", "/etc/mongod.conf"]
