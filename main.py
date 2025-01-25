import logging
from typing import List
import tempfile
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
import requests
from io import BytesIO

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot token
TOKEN = "token"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Welcome to Image to PDF Bot! 👋\n\n'
        'Send me one or multiple images, and I\'ll convert them into a PDF file.\n\n'
        'Commands:\n'
        '/start - Show this message\n'
        '/convert - Convert collected images to PDF\n'
        '/cancel - Clear collected images'
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear the user's collected images."""
    if 'images' in context.user_data:
        context.user_data['images'] = []
    await update.message.reply_text('All collected images have been cleared. You can start fresh!')

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Convert collected images to PDF."""
    if 'images' not in context.user_data or not context.user_data['images']:
        await update.message.reply_text('No images to convert! Please send me some images first.')
        return
    
    status_message = await update.message.reply_text('Converting images to PDF...')
    
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download and convert all images
            images = []
            for image_file in context.user_data['images']:
                img = Image.open(BytesIO(image_file))
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                images.append(img)
            
            # Save as PDF
            pdf_path = os.path.join(temp_dir, f'output_{update.effective_user.id}.pdf')
            if images:
                first_image = images[0]
                if len(images) > 1:
                    first_image.save(pdf_path, save_all=True, append_images=images[1:])
                else:
                    first_image.save(pdf_path)
                
                # Send PDF file
                with open(pdf_path, 'rb') as pdf_file:
                    await update.message.reply_document(
                        document=pdf_file,
                        filename='converted_images.pdf',
                        caption='Here\'s your PDF file! 📄'
                    )
                
                # Clear session
                context.user_data['images'] = []
                await status_message.edit_text('Conversion completed successfully!')
    
    except Exception as e:
        logger.error(f'Error converting to PDF: {e}')
        await status_message.edit_text(
            'done'
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming photos."""
    try:
        # Get the photo file
        photo = await update.message.photo[-1].get_file()
        image_bytes = await photo.download_as_bytearray()
        
        # Initialize or update user session
        if 'images' not in context.user_data:
            context.user_data['images'] = []
        
        context.user_data['images'].append(image_bytes)
        
        await update.message.reply_text(
            f'Image received! ({len(context.user_data["images"])} total)\n\n'
            'Send more images or use /convert to create PDF'
        )
    
    except Exception as e:
        logger.error(f'Error processing photo: {e}')
        await update.message.reply_text(
            'Sorry, there was an error processing your image. Please try again.'
        )

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("convert", convert))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
