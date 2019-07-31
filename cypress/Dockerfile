FROM cypress/base:10

RUN mkdir /cypress

COPY . /cypress

WORKDIR /cypress

RUN npm install --save cypress cypress-log-to-output

RUN ls

RUN pwd

RUN ./node_modules/.bin/cypress run --config baseUrl=http://nginx