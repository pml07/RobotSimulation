FROM python:3.7

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r  /tmp/requirements.txt --no-cache-dir

COPY . /app
WORKDIR /app

CMD python -u main.py