FROM mongo:7.0.14

# enable file logging
# USER root
# RUN mkdir -p /var/log/mongodb \
#     && chown -R mongodb:mongodb /var/log/mongodb

USER mongodb
CMD ["-f", "/etc/mongod.conf"]
