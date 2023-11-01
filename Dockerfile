# Use the official Python image as the base image
FROM python:3.8-slim

RUN python -m pip install rasa

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

RUN rasa train nlu

# Specify the user which should be used to execute all commands below
USER root

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy the supervisord configuration file into the container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the ports that the Rasa server and action server will use
EXPOSE 5005 5055

# Start supervisord to manage Rasa server and Action server processes
CMD ["/usr/bin/supervisord"]
