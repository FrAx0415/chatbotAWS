FROM nginx:latest

# Espone la porta su cui Nginx sarà in ascolto
EXPOSE 80

# Comando per avviare Nginx
CMD ["nginx", "-g", "daemon off;"]
