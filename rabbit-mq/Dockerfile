FROM rabbitmq:3.13.7-management

ARG DEFAULT_PORT

RUN echo "listeners.tcp.default = ${DEFAULT_PORT}" >> /etc/rabbitmq/rabbitmq.conf \
    echo "management.tcp.port = 1${DEFAULT_PORT}" >> /etc/rabbitmq/rabbitmq.conf
