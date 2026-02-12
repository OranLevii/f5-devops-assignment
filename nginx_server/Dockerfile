# Uses Ubuntu 24.04 as the base image
FROM ubuntu:24.04

# Update lists. Install nginx. Delete lists to save space
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Copy hosts custom config file to the container    
COPY nginx.conf /etc/nginx/nginx.conf

# Start nginx in the foreground so the container doesnt exit
CMD ["nginx", "-g", "daemon off;"]
