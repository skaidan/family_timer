FROM nginx:1.27-alpine

COPY family_timer.html /usr/share/nginx/html/index.html
COPY data /usr/share/nginx/html/data

EXPOSE 80