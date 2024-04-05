# Telegram Notifier

This script implements a Flask-based web server that allows sending messages and photos to a Telegram Bot using HTTP requests. It also exposes metrics for monitoring purposes.

## Description

The script includes the following components:

- Flask web server: Handles HTTP requests for sending messages and photos to a Telegram Bot.
- TelegramNotifier class: Manages communication with the Telegram Bot API.
- Metrics collector: Collects and exposes prometheus-metrics for monitoring.

## How to Use

### For the Run part, the following env-vars need to be set respectively before running the container

- TZ=<YOUR_TIMEZONE>
- TELEGRAM_BOT_CHANNEL_URL=<https://api.telegram.org/bot>[YOUR_TELEGRAM_BOT_TOKEN]
- TELEGRAM_CHAT_ID=<YOUR_TELEGRAM_CHAT_ID>

   1. Clone and Run
      - Clone this git repository.

      ````shell
      git clone <repository_url>
      ````

      - Build the Docker image.

      ````shell
      docker build -t <IMAGE_TAG> .
      ````

      - Run the docker container.

      ````shell
      docker run -d -p 5000:5000 -e TELEGRAM_BOT_CHANNEL_URL=<your_telegram_bot_channel_url> -e TELEGRAM_CHAT_ID=<your_telegram_chat_id> -e TZ=<YOUR_TIMEZONE> bladethazar/telegram-notifier
      ````

   2. Pull and Run
      - Pull the docker image from Docker Hub.
        - <https://hub.docker.com/repository/docker/bladethazar/telegram-notifier/>
      - Run the container directly.

      ````shell
      docker run -d -p 5000:5000 -e TELEGRAM_BOT_CHANNEL_URL=<your_telegram_bot_channel_url> -e TELEGRAM_CHAT_ID=<your_telegram_chat_id> -e TZ=<YOUR_TIMEZONE> bladethazar/telegram-notifier
      ````

## Endpoint description

### /send_message

This endpoint is used to send a message.

- Request Method
  - POST

- Request Body
  - Content-Type: application/json
  - message (string, required): The message to be sent.

- Response
  - Status: 200
  - Content-Type: application/json
  - message (string): The telegram-channel the message was sent to.

### /send_photo

This endpoint allows you to send a photo with an optional caption. The request should be sent as a POST to the specified URL.

- Request Body

  The request body should be of form-data type and contain the following parameters:

  - `photo` (file): The photo to be sent.
  - `caption` (text): An optional caption for the photo.

- Response
  - Upon successful execution, the endpoint will return a JSON response with a status code of 200 and a message indicating the result of the operation.

  Example:

  ````json
  {
      "message": "Photo sent successfully to Telegram Bot-Channel [YOUR_TELEGRAM_CHANNEL]"
  }
  ````

### /metrics

This endpoint is used expose prometheus-metrics.

- Request Method

  - GET

- Response
  - Status: 200
  - Content-Type: text/plain

  Example:

  ````text
  # HELP telegram_photos_sent_total Total number of photos sent
  # TYPE telegram_photos_sent_total counter
  telegram_photos_sent_total 1.0
  ````
