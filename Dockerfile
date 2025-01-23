# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y vim nodejs npm && \
    apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install django
RUN pip install -r requirements.txt

# Install Node.js dependencies
RUN npm install -g npm@latest
RUN npm install

# Expose ports
EXPOSE 5734
EXPOSE 8020

# Set environment variables
ENV LANG en_US.utf8

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8020"]