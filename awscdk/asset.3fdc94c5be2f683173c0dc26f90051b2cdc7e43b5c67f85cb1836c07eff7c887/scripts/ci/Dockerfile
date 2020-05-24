# this image is tagged and pushed to the production registry (such as ECR)
FROM python:3.8 as production
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY backend/requirements/base.txt /code/requirements/
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements/base.txt
COPY backend/scripts/prod/start_prod.sh \
    backend/scripts/dev/start_ci.sh \
    backend/scripts/dev/start_asgi.sh \
    /
ADD backend/ /code/

# build stage that generates quasar assets
FROM node:10-alpine as build-stage
ENV FULL_DOMAIN_NAME localhost:9000
WORKDIR /app/
COPY quasar/package.json /app/
RUN npm cache verify
RUN npm install -g @quasar/cli
RUN npm install --progress=false
COPY quasar /app/
RUN quasar build -m pwa

# this stage is used for integration testing
FROM production as gitlab-ci
# update and install nodejs
COPY --from=build-stage /app/dist/pwa/index.html /code/templates/
COPY --from=build-stage /app/dist/pwa /static

COPY cypress.json /code

RUN mkdir /code/cypress
COPY cypress/ /code/cypress/

RUN apt-get -qq update && apt-get -y install nodejs npm
RUN node -v
RUN npm -v

# cypress dependencies
RUN apt-get -qq install -y xvfb \
    libgtk-3-dev \
    libnotify-dev \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2
