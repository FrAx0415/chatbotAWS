FROM nginx:latest

# Copia il contenuto della cartella nel directory di Nginx
COPY . /usr/share/nginx/html

# Espone la porta su cui Nginx sarà in ascolto
EXPOSE 80

# Comando per avviare Nginx
CMD ["nginx", "-g", "daemon off;"]
