FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY requirements/base.txt /code/requirements/
RUN pip install -r requirements/base.txt
COPY scripts/prod/start_prod.sh scripts/dev/start_ci.sh /
ADD . /code/