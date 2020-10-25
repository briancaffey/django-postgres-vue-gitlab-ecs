FROM node:12.19.0

WORKDIR /app/

COPY . .

RUN npm install -g @quasar/cli && \
    npm install -g @vue/cli && \
    npm install -g @vue/cli-init

COPY start_dev.sh .

CMD ["/app/start_dev.sh"]