FROM node:10.14.2-jessie

# make the 'app' folder the current working directory
WORKDIR /app/

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# expose port 8080 to the host
EXPOSE 8080

CMD ["sh", "start_dev.sh"]