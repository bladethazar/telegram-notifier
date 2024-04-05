# Use an official Python runtime as a parent image
FROM --platform=linux/arm64 python:3.12.0rc2-slim as build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOSTNAME="telegram-notifier"
ENV PORT="5000"
# Set default timezone
ENV TZ="Europe/Berlin"

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port on which your Flask app runs
EXPOSE 5000

# Command to run the Flask application
CMD ["python3", "app/telegram_notifier.py"]
