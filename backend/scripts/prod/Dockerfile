FROM python:3.8 as production
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
RUN useradd -m app
USER app
WORKDIR /code
COPY --chown=app:app requirements/base.txt /code/requirements/
ENV PATH="/home/app/.local/bin:${PATH}"
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements/base.txt
ADD --chown=app:app . /code/
