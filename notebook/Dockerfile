FROM quay.io/jupyter/pyspark-notebook:spark-3.5.3

ARG JUPYTER_HASHED_PASSWORD

RUN echo "c.PasswordIdentityProvider.hashed_password = u'$JUPYTER_HASHED_PASSWORD'" >> /home/jovyan/.jupyter/jupyter_server_config.py
