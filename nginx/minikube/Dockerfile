# build stage
FROM node:10-alpine as build-stage
ARG DOMAIN_NAME
ARG GOOGLE_OAUTH2_KEY
ARG GITHUB_KEY
ARG WS_PROTOCOL
ARG HTTP_PROTOCOL

ENV DOMAIN_NAME=${DOMAIN_NAME}
ENV GOOGLE_OAUTH2_KEY=${GOOGLE_OAUTH2_KEY}
ENV GITHUB_KEY=${GITHUB_KEY}
ENV WS_PROTOCOL=${WS_PROTOCOL}
ENV HTTP_PROTOCOL=${HTTP_PROTOCOL}

WORKDIR /app/
COPY quasar/package.json /app/
RUN npm cache verify
RUN npm install -g @quasar/cli
RUN npm install --progress=false
COPY quasar /app/
RUN quasar build -m pwa

# ci stage
FROM nginx:1.13.12-alpine as ci-stage
COPY nginx/minikube/minikube.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist/pwa /dist/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
