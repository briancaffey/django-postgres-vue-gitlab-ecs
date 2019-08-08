#!/bin/bash

# install project dependencies
cd documentation

npm install

npm install -D @vuepress/plugin-google-analytics @vuepress/plugin-pagination

# build vuepress files
yarn run docs:build