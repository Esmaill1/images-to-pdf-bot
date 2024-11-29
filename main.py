import os
##import dotenv
import requests
import img2pdf
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
##dotenv.load_dotenv()
TOKEN = "7289833807:AAFOqKJCMDlr2aIdiGVv-L6AYmlLRsQEprQ"

# Bot username
BOT_USERNAME: Final = '@image_to_pdfs_bot'

# Temporary storage for image paths
user_images = {}

# Command: /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello there! I'm a bot that converts multiple images into a single PDF.\n"
        "Upload images one by one, and type /done when you're finished."
    )

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "To use me:\n1. Upload images one by one.\n2. Type /done to combine them into a PDF."
    )

# Convert images to PDF and send it back
async def convert_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Combine the user's images into a single PDF."""
    chat_id = update.message.chat_id

    # Check if the user has uploaded any images
    if chat_id not in user_images or not user_images[chat_id]:
        await update.message.reply_text("You haven't uploaded any images. Please upload images first.")
        return

    # Combine images into a single PDF
    pdf_file_path = f"{chat_id}_output.pdf"
    with open(pdf_file_path, 'wb') as f:
        f.write(img2pdf.convert(user_images[chat_id]))

    # Send the PDF to the user
    await context.bot.send_document(chat_id=chat_id, document=open(pdf_file_path, 'rb'))

    # Clean up temporary files
    for image_path in user_images[chat_id]:
        os.remove(image_path)
    os.remove(pdf_file_path)
    user_images[chat_id] = []  # Reset the user's images

    await update.message.reply_text("Here is your PDF!")

# Handle uploaded photos
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo uploads and save them locally."""
    chat_id = update.message.chat_id
    photo = update.message.photo[-1].file_id
    received_file = await context.bot.get_file(photo)
    file_path = f"{chat_id}_{len(user_images.get(chat_id, []))}.jpg"

    # Download and save the image
    with open(file_path, 'wb') as f:
        f.write(requests.get(received_file.file_path).content)

    # Add the image to the user's list
    if chat_id not in user_images:
        user_images[chat_id] = []
    user_images[chat_id].append(file_path)

    await update.message.reply_text("Image received! Upload more or type /done to create the PDF.")

# Handle basic text responses
def handle_response(text: str, update: Update) -> str:
    processed: str = text.lower()
    if 'hi' in processed:
        return f"Hi {update.message.chat.first_name}, how are you?"
    if 'how are you' in processed:
        return "I'm good!"
    return "Sorry, I don't understand."

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text, update)
        else:
            return
    else:
        response: str = handle_response(text, update)

    await update.message.reply_text(response)

# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Main function to run the bot
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('done', convert_to_pdf))  # /done to generate PDF

    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))  # Handle photo uploads

    # Error handler
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=5)
