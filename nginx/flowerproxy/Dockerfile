FROM nginx:1.19.3-alpine
COPY proxy.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]