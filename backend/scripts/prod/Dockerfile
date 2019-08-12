# build stage that generates quasar assets
FROM node:10-alpine as build-stage
ENV HTTP_PROTOCOL http
ENV WS_PROTOCOL ws
ENV DOMAIN_NAME localhost:8000
WORKDIR /app/
COPY quasar/package.json /app/
RUN npm cache verify
RUN npm install -g @quasar/cli
RUN npm install --progress=false
COPY quasar /app/
RUN quasar build -m pwa

# this image is tagged and pushed to the production registry (such as ECR)
FROM python:3.7 as production
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
ADD backend /code/

# this stage is used for integration testing
FROM production as gitlab-ci
# cypress dependencies
# RUN apt-get -qq update
# RUN apt-get -qq install -y xvfb libgtk-3-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2
# add static files from build
COPY --from=build-stage /app/dist/pwa/index.html /code/templates/
# COPY --from=build-stage /app/dist/pwa /code/static
COPY --from=build-stage /app/dist/pwa /static
# index.html is listed here
RUN ls /code/templates/ -al
# also tried this, but still nothing in the templates directory when the container is started
RUN cp /static/index.html /code/templates/index.html
