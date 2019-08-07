#!/bin/bash

# https://docs.npmjs.com/cli/cache
npm cache verify

# install project dependencies
npm install

npm install -D @vuepress/plugin-google-analytics @vuepress/plugin-pagination
# build vuepress files
yarn run docs:dev