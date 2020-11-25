FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
RUN useradd -m app
USER app
WORKDIR /code
COPY --chown=app:app requirements/base.txt requirements/dev.txt requirements/test.txt /code/requirements/
ENV PATH="/home/app/.local/bin:${PATH}"
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements/base.txt \
    && pip install -r requirements/dev.txt \
    && pip install -r requirements/test.txt
ADD --chown=app:app . /code/
