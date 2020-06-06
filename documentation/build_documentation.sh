#!/bin/bash

# install project dependencies
cd documentation

npm install

# build vuepress files
yarn run docs:build