FROM python:3.9.11

WORKDIR /opt/harvester
COPY ./* ../../app/config.py ./

RUN pip3 install -U pip \
    && pip3 install -r requirements.txt

CMD python3 -m harvester
