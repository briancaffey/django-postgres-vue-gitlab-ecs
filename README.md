## Architecture

![png](/draw.png)

## Local Development

```
docker-compose up --build
```

Open `http://localhost` in your browser

You can specify environment variables for docker-compose by adding an `.env` file to the root of the project based on `.env.template`.

### Access Django Shell in Jupyter Notebook

With all containers running, run the following commands:

```
docker exec -it backend bash
# cd notebooks/
# ../manage.py shell_plus --notebook
```

or use this single command:

```
docker exec -it backend bash -c 'cd notebooks && ../manage.py shell_plus --notebook'
```