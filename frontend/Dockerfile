FROM nginx:alpine

# Apaga a configuração default do nginx
RUN rm -rf /usr/share/nginx/html/*

# Copia seus arquivos HTML/JS/CSS para o local que o nginx serve
COPY . /usr/share/nginx/html/frontend

# Expor a porta 
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]