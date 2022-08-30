FROM python:3.5

ENV WEBAPP_DIR=/backend

RUN mkdir $WEBAPP_DIR
WORKDIR $WEBAPP_DIR

ADD requirements.txt $WEBAPP_DIR/
RUN pip install -r requirments.txt
