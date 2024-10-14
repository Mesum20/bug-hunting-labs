# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir flask

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Ensure the db directory exists in the container
RUN mkdir -p /app/db

# Copy the backup.sql file to the /app/db directory
COPY db/backup.sql /app/db/

# Run the app. Use 0.0.0.0 to ensure the app is accessible from outside the container
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
