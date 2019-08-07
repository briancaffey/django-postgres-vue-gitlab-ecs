## Frontend

Let's create a new feature branch to start work on our frontend:

```
git checkout -b feature-vue develop
```

This will make a new branch called `feature-vue` that will branch off of the `develop` branch.

What we want to do next is add a `frontend` folder to the base of our project that will contain all of our code for the frontend VueJS application. One way to do this is to create a `nodejs` container and use Vue CLI 3, a command line tool for starting VueJS applications. When we create the container, let's mount the `frontend` and run `/bin/sh` so we can run commands at the terminal inside our `nodejs` container.

Run the following command from the base of our project:

```
mkdir frontend
docker run --rm -it -v ~/gitlab/verbose-equals-true/frontend:/code node:9.11.1-alpine /bin/sh
```

We are now in the nodejs container. From here we can install `vue` and `vue-cli-3` and create our Vue application. Run the following commands inside the container:

```
# cd code
# npm i -g vue @vue/cli
# vue create .
```

Here's the full output:

```
docker run --rm -it -v ~/gitlab/verbose-equals-true/frontend:/code node:9.11.1-alpine /bin/sh
Unable to find image 'node:9.11.1-alpine' locally
9.11.1-alpine: Pulling from library/node
605ce1bd3f31: Pull complete
7cc38010b685: Pull complete
88a635599bc5: Pull complete
Digest: sha256:f8f6c69cce180a9a7c9fa685c86671b1e1f2ea7cc5f9a0dbe99d30cc7a0b6cbe
Status: Downloaded newer image for node:9.11.1-alpine
/ # cd code/
/code # npm i -g vue @vue/cli
/usr/local/bin/vue -> /usr/local/lib/node_modules/@vue/cli/bin/vue.js

> protobufjs@6.8.8 postinstall /usr/local/lib/node_modules/@vue/cli/node_modules/protobufjs
> node scripts/postinstall


> nodemon@1.18.5 postinstall /usr/local/lib/node_modules/@vue/cli/node_modules/nodemon
> node bin/postinstall || exit 0

Love nodemon? You can now support the project via the open collective:
 > https://opencollective.com/nodemon/donate

npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.4 (node_modules/@vue/cli/node_modules/fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.4: wanted {"os":"darwin","arch":"any"} (current: {"os":"linux","arch":"x64"})

+ @vue/cli@3.0.5
+ vue@2.5.17
added 631 packages in 43.452s
/code # vue create .
```

After you run `vue create .`, you will be prompted to make decisions for your Vue Project. Let's choose the following options:

- Create the project in the current folder? `Y`
- Please pick a preset: `Manually select features`
- Check the features needed for your project: (select all except for TypeScript)
  - Babel
  - PWA
  - Router
  - Vuex
  - CSS Pre-processors
  - Linter /Formatter
  - Unit Testing
  - E2E Testing
- User history mode for router? `Y`
- Pick a CSS pre-processor `Sass/SCSS`
- Pick a linter / formatter config: `ESLint + Airbnb config`
- Pick additional lint features: `Lint on save`
- Pick a unit testing solution: `Jest`
- Pick a E2E testing solution: `Nightwatch (Selenium-based)`
- Where do you prefer placing config for Babel, PostCSS, ESLint, etc.? `In package.json`
- Save this as a preset for future projects? `N`
- Pick the package manager to use whne installing dependencies: `Use NPM`

Notice that the router options gave us a message: `Requires proper server setup for index fallback in production`. We will address this later on when we integrate our frontend with our backend and webserver.

You should now see that the the project was created inside of the `frontend` folder. Let's change permissions for these files since they were created by docker as root:

```
sudo chown -R $USER:$USER .
```

Let's make one small but important change to the `.gitignore` file that was generated when we created the Vue application:

```
node_modules/*
!node_modules/.gitkeep
```

Inside of `.gitkeep`, let's include the following link for reference:

```
https://www.git-tower.com/learn/git/faq/add-empty-folder-to-version-control
```

We are now almost ready to start developing our Vue app. But before we do that, we need to talk about environments. One of the main reasons for using docker is so that we can have the same environment for local development, staging servers, testing, and production (and perhaps even other environments such as a `debug` environment).

A VueJS app is nothing more than a `collection of static files`. However, when we develop our VueJS app, we will be working with `.vue` files that take advantage of modern Javascript features (ES6). When we run `npm run build`, the `.vue` files and other files are bundled into a `collection of static files` that are delivered to the browser, so they don't include `.vue` files; they only `.html`, `.js` and `.css` files.

We also want to take advantage of hot-reloading. This is a feature of modern Javascript frameworks and tools like webpack that allows us to view the changes we make in our app in the browser as we save changes in our code editor. This means that we can make changes to `.vue` files, and then we will be able to see changes instantly in a browser that is showing us a preview. This "preview" is started by running `npm run serve`. This is the mode that we will use as we develop our app. It is not using the `collection of static files` that we will use in production, but the application's behavior when using `npm run serve` is very similar to the application that we get when we generate the `collection of static files`.

Since docker is all about maintaining the same environment between development, testing, staging/QA and prodcution, we need to be careful when we start introducing different environments. It wouldn't be practical to run `npm run build` after every change we made while developing our app; this command takes some time to generate the `collection of static files`. So although it is breaking a core principle of docker, using different environments for local development and production is necessary for our application.

What this means is that we will ultimately need two different versions of our existing `docker-compose.yml` file:

1. One that serves a `collection of static files` for production, and
2. One that offers us hot reloading during our development process via a `nodesj` server

We actually *will also* be able to use verion `1` during local development, but our changes won't be reflected immediately. We'll see all of this in action very soon.

Before we split our `docker-compose.yml` into a development version and a production version, let's commit our changes.

```
git add .
git commit -m "added vuejs app in frontend"
```

Next, let's create `docker-compose.dev.yml`:

```
cp docker-compose.yml docker-compose.dev.yml
```

We will need to introduce two new services in `docker-compose.dev.yml`: `frontend` and `nginx`. We will also introduce a [network](https://docs.docker.com/network/) that will help our services communicate through the docker engine. (We'll explore this soon).

### Networks

There are several types of networks that docker supports, but we will use one called "user-defined bridge networks".

> User-defined bridge networks are best when you need multiple containers to communicate on the same Docker host. We will add these to `docker-compose.dev.yml` after we add the `frontend` and `nginx` services.

More information on docker networks can be found [here](https://docs.docker.com/network/).

### `frontend` service

`frontend` will use a `node` base image and it will run `npm run serve` so that we can watch for changes to files in our project and see the result instantly.

Here's what the service will look like in `docker-compose.dev.yml`:

```yml
  frontend:
    build:
      context: ./frontend
    volumes:
      - ./frontend:/app/frontend:ro
      - '/app/node_modules'
    ports:
      - "8080:8080"
    networks:
      - main
    depends_on:
      - backend
      - db
    environment:
      - NODE_ENV=development
```

For this service, we will be looking for a `Dockerfile` in `frontend`. We know this from the `build/context` part of the service definition:

```yml
    build:
      context: ./frontend
```

Let's create this `Dockerfile`, and then continue looking at the `frontend` service in `docker-compose.dev.yml`.

### `frontend` Dockerfile

```
FROM node:9.11.1-alpine

# make the 'app' folder the current working directory
WORKDIR /app/

# copy package.json to the /app/ folder
COPY package.json ./

# https://docs.npmjs.com/cli/cache
RUN npm cache verify

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# expose port 8080 to the host
EXPOSE 8080

# run the development server
CMD ["npm", "run", "serve"]
```

This Dockerfile says:

- `FROM node:9.11.1-alpine` Use the base image of `node:9.11.1-alpine`,
- `WORKDIR /app/` In the container, create a folder in the root of the filesystem called `/app` and move into this directory
- `COPY package.json ./` Copy `package.json` from our local machine into `/app` (not `/`) in the container
- `RUN npm install` Install the dependencies into `node_modules`,
- `COPY . .` Copy over all of the files from our project to `.`, which is `/app` since we set that as `WORKDIR`,
- `WORKDIR /app/frontend` Change into the folder `/app/frontend` in the container
- `EXPOSE 8080` Expose port `8080` in the container
- `CMD ["npm", "run", "serve"]` Run `npm run serve` in the container

This Dockerfile would work, but there are some small optimizations that we can make to improve our workflow.

Here's the optimized Dockerfile:

```
FROM node:9.11.1-alpine

# make the 'app' folder the current working directory
WORKDIR /app/

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# expose port 8080 to the host
EXPOSE 8080

CMD ["sh", "start_dev.sh"]
```

Notice that at the end of the Dockerfile we are running `start_dev.sh`. Let's create `start_dev.sh` as a script in the top level of the `frontend` folder:

```
#!/bin/bash

# https://docs.npmjs.com/cli/cache
npm cache verify

# install project dependencies
npm install

# run the development server
npm run serve
```

Let's continue looking at `docker-compose.dev.yml`:

```yml
    volumes:
      - ./frontend:/app/:ro
      - '/app/node_modules'
```

After the `build` section, we see that we mount two volumes. **First**, we mount the `frontend` directory from our local machine into `/app/frontend`. `ro` specifies that the mounted volume is read-only. This is fine since we will be editing the files in this volume from our local machine, not from inside of the docker container.

**Second**, we mount `/app/node_modules`. This will make sure that `node_modules` is not overwritten when mounting files into the `frontend` container. You can read more about why this is the case in [this Stack Overflow post](https://stackoverflow.com/questions/30043872/docker-compose-node-modules-not-present-in-a-volume-after-npm-install-succeeds).

Next, we see that the service definition for `frontend` lists `main` under networks. This means that the service shares a network with other services that are also on the `main` network. We will see why this is the case soon.

The `depends_on` section specifies that `db` and `backend` must start before `frontend` is started.

Let's run `docker-compose` with our new `docker-compose.dev.yml` to do a quick test:

Let's add a `networks` section to the very bottom of `docker-compose.dev.yml`:

```yml
networks:
  main:
    driver: bridge
```

Our `docker-compose.dev.yml` file should now look like this:

```yml
version: '3'

services:
  db:
    container_name: db
    image: postgres
    networks:
      - main

  backend:
    container_name: backend
    build: ./backend
    command: /start.sh
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    networks:
      - main
    depends_on:
      - db

  frontend:
    container_name: frontend
    build:
      context: ./frontend
    volumes:
      - ./frontend:/app/frontend:ro
      - '/app/node_modules'
    ports:
      - "8080:8080"
    networks:
      - main
    depends_on:
      - backend
      - db
    environment:
      - NODE_ENV=development

networks:
  main:
    driver: bridge
```

Let's run docker-compose to bring up the network and the containers:

```
docker-compose -f docker-compose.dev.yml up --build
```

We should now be able to see both the Vue application and the Django application by visiting:

- `localhost:8000/admin` for Django
- `localhost:8080` for Vue

Let's commit our changes before we add `nginx`.

```
git add .
git commit -m "added docker-compose.dev.yml and a dockerfile for frontend"
```
