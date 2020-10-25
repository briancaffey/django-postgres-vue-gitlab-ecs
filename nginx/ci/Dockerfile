# build stage
FROM node:10-alpine as build-stage
WORKDIR /app/
COPY quasar/package.json /app/
RUN npm cache verify
RUN npm install -g @quasar/cli
RUN npm install --progress=false
COPY quasar /app/
RUN quasar build -m pwa

# ci stage
FROM nginx:1.19.3-alpine as ci-stage
COPY nginx/ci/ci.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist/pwa /dist/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
