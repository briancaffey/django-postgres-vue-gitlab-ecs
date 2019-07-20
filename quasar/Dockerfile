FROM node:8

WORKDIR /app/

COPY . .

RUN npm install -g @quasar/cli && \
    npm install -g @vue/cli && \
    npm install -g @vue/cli-init

EXPOSE 8080

WORKDIR /app/quasarfrontend

RUN yarn

CMD quasar dev