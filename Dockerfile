# Use the official Python image as the base image
FROM python:3.8-slim-buster

RUN python -m pip install rasa

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

RUN rasa train nlu

# Specify the user which should be used to execute all commands below
USER 1001

# Expose the ports that the Rasa server and action server will use
EXPOSE 5005 5055

# Start the Rasa server and action server
CMD ["rasa", "run", "--cors", "*", "--enable-api", "&", "rasa", "run", "actions"]
