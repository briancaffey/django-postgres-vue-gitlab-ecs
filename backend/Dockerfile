FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD notebooks/jupyter_notebook_config.py /root/.jupyter/
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 8000
CMD ["sh", "/code/start.sh"]