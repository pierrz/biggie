FROM quay.io/jupyter/pyspark-notebook:spark-3.5.3

ARG JUPYTER_HASHED_PASSWORD \
    JUPYTER_SUBDOMAIN

ENV CONFIG_PATH=/home/jovyan/.jupyter/jupyter_server_config.py

RUN echo "c.PasswordIdentityProvider.hashed_password = u'$JUPYTER_HASHED_PASSWORD'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.base_url = '/lab'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.allow_origin = 'https://$JUPYTER_SUBDOMAIN'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.allow_origin_pat = 'https://.*'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> $CONFIG_PATH && \
    echo "c.NotebookApp.port = 8888" >> $CONFIG_PATH && \
    echo "c.NotebookApp.open_browser = False" >> $CONFIG_PATH && \
    echo "c.NotebookApp.trust_xheaders = True" >> $CONFIG_PATH && \
    echo "c.NotebookApp.websocket_url = 'wss://$JUPYTER_SUBDOMAIN'" >> $CONFIG_PATH

RUN pip install --no-cache-dir jupyterlab-git

CMD jupyter lab --debug
