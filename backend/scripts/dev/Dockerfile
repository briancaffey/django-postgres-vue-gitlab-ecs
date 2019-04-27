FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY requirements/base.txt requirements/dev.txt requirements/test.txt /code/requirements/
RUN pip install -r requirements/base.txt \
        && pip install -r requirements/dev.txt \
        && pip install -r requirements/test.txt
COPY scripts/dev/start_dev.sh scripts/dev/start_beat.sh scripts/dev/start_asgi.sh /
ADD . /code/