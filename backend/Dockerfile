FROM python:3.10

ENV WEBAPP_DIR=/backend

RUN mkdir $WEBAPP_DIR
WORKDIR $WEBAPP_DIR

ADD requirements.txt $WEBAPP_DIR/
RUN pip install --upgrade pip
RUN python3 -m pip install channels_redis
RUN python -m pip install -U channels
RUN pip install django
#RUN pip install -r requirements.txt
