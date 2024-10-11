FROM quay.io/jupyter/pyspark-notebook:spark-3.5.3

ARG JUPYTER_PASSWORD

RUN echo "c.ServerApp.password = u'$JUPYTER_PASSWORD'" >> /home/jovyan/.jupyter/jupyter_server_config.py
