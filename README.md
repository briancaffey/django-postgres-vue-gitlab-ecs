Build the backend container with:

```
docker build -t briancaffey.com:latest .
```

Run the backend container with:

```
docker run -it -v /home/brian/gitlab/briancaffey.com/backend/:/code briancaffey
.com:latest /bin/bash
```