# build stage
FROM node:10-alpine as build-stage
ARG FULL_DOMAIN_NAME
ARG GOOGLE_OAUTH2_KEY
ARG GITHUB_KEY

ENV FULL_DOMAIN_NAME=${DOMAIN_NAME}
ENV GOOGLE_OAUTH2_KEY=${GOOGLE_OAUTH2_KEY}
ENV GITHUB_KEY=${GITHUB_KEY}

WORKDIR /app/
COPY quasar/package.json /app/
RUN npm cache verify
RUN npm install -g @quasar/cli
RUN npm install --progress=false
COPY quasar /app/
RUN quasar build -m pwa

# ci stage
FROM nginx:1.18.0-alpine as ci-stage
COPY nginx/minikube/minikube.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist/pwa /dist/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
