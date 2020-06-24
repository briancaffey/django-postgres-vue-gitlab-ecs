#!/bin/bash

# install project dependencies
cd documentation

npm install

# build vuepress files
npm run docs:build