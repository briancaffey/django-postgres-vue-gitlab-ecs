# build stage
FROM node:10-alpine as build-stage
WORKDIR /app/
ENV DOMAIN_NAME 192.168.99.105:30958
ENV GITHUB_KEY github123
ENV GOOGLE_OAUTH2_KEY google123
ENV HTTP_PROTOCOL http
COPY quasar/package.json /app/
RUN npm cache verify
RUN npm install -g @quasar/cli
RUN npm install --progress=false
COPY quasar /app/
RUN quasar build -m pwa

# minikube stage
FROM nginx:1.13.12-alpine as minikube
COPY nginx/minikube/minikube.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist/pwa /dist/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
