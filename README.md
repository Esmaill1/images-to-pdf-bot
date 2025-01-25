
# Image to PDF Bot 📸➡️📄

This Telegram bot allows users to upload one or more images, which are then converted into a PDF. It provides an easy-to-use interface with commands for managing and converting images into a PDF file.

## Features
- **Image Collection**: Accepts multiple images from users.
- **Image to PDF Conversion**: Combines all uploaded images into a single PDF.
- **Session Management**: Allows users to clear their collected images and start fresh.
- **Error Handling**: Handles errors gracefully, providing helpful feedback to users.

## Commands
- `/start`: Displays a welcome message and an overview of commands.
- `/convert`: Converts all collected images into a PDF file.
- `/cancel`: Clears all collected images, resetting the session.

## Requirements
- **Python 3.7+**
- Telegram Bot API token (get yours from [BotFather](t.me/BotFather))
- Required Python libraries:
  - `python-telegram-bot`
  - `Pillow`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/image-to-pdf-bot.git
   cd image-to-pdf-bot
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Replace the `TOKEN` in the script with your bot token from BotFather:
   ```python
   TOKEN = "your-telegram-bot-token"
   ```

## Usage
1. Start the bot:
   ```bash
   python images_to_pdf_bot.py
   ```

2. Open Telegram, search for your bot, and click **Start**.

3. Send images to the bot. Use `/convert` to get a PDF of the uploaded images.

4. To clear all uploaded images, use `/cancel`.

## Deployment
This bot can be hosted on any platform that supports Python, such as:
- [Heroku](https://heroku.com/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Google Cloud Run](https://cloud.google.com/run)

### Example Deployment on Heroku
1. Install the Heroku CLI and log in:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create
   ```

3. Push the code to Heroku:
   ```bash
   git push heroku main
   ```

4. Set the bot token as a config variable:
   ```bash
   heroku config:set TOKEN=your-telegram-bot-token
   ```

5. Start the bot:
   ```bash
   heroku ps:scale worker=1
   ```

## Contributing
Feel free to submit issues or create pull requests for bug fixes or new features.

## License
This project is licensed under the MIT License.
