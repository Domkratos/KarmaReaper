# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install required packages
RUN pip install --no-cache-dir praw discord.py python-dotenv

# Run the bot script when the container launches
CMD ["python", "./karma-reaper.py"]
