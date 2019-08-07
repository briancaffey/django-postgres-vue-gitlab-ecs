FROM node:alpine
WORKDIR /app/
COPY ./package.json .
COPY ./start*.sh ./
RUN mkdir docs
COPY ./docs ./docs
