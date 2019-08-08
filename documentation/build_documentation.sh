#!/bin/bash

# install project dependencies
ls

pwd

npm install

npm install -D @vuepress/plugin-google-analytics @vuepress/plugin-pagination

# build vuepress files
yarn run docs:build