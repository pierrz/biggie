# TODO: go through all config parameters to be sure it is all relevant/required
# (at least it is working though ...)

# python-3.12  spark-3.5.3
FROM quay.io/jupyter/pyspark-notebook:spark-3.5.3

ARG JUPYTER_HASHED_PASSWORD \
    HOST_USER_UID

ENV CONFIG_PATH=/home/jovyan/.jupyter/jupyter_server_config.py

RUN echo "c.PasswordIdentityProvider.hashed_password = u'$JUPYTER_HASHED_PASSWORD'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.port = 11000" >> $CONFIG_PATH && \
    echo "c.NotebookApp.open_browser = False" >> $CONFIG_PATH && \
    echo "c.NotebookApp.trust_xheaders = True" >> $CONFIG_PATH && \
    echo "c.NotebookApp.base_url = '/'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.allow_credentials = True" >> $CONFIG_PATH && \
    # Allow WebSocket connections from proxy
    # echo "c.NotebookApp.allow_origin = 'https://$JUPYTER_SUBDOMAIN'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.allow_origin = '*'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.allow_origin_pat = 'https://.*'" >> $CONFIG_PATH && \
    # Don't try to authenticate WebSocket connections
    echo "c.NotebookApp.disable_check_xsrf = True" >> $CONFIG_PATH && \
    # Set proper WebSocket URL
    # echo "c.NotebookApp.websocket_url = 'wss://$JUPYTER_SUBDOMAIN'" >> $CONFIG_PATH \
    echo "c.NotebookApp.websocket_url = ''" >> $CONFIG_PATH && \
    # Allow requests from proxy
    echo "c.NotebookApp.allow_remote_access = True" >> $CONFIG_PATH && \
    # Optional: increase timeouts
    echo "c.NotebookApp.kernel_ws_protocol = 'ws'" >> $CONFIG_PATH

RUN /opt/conda/bin/conda install jupyterlab-git

USER root
RUN usermod -u $HOST_USER_UID jovyan && groupmod -g $HOST_USER_UID users
RUN mkdir -p /home/jovyan/work && chown -R jovyan:users /home/jovyan
# RUN apt update && apt install -y net-tools iputils-ping netcat-traditional

USER jovyan
# --ip=0.0.0.0 --no-browser
CMD jupyter lab --port=11000 --debug
