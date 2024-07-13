import logging
import csv
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import os
from tokens import TOKEN
from groupImages import createGroupImage

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define states for the conversation handler
ENTER_BKMS_ID = 1
MESSAGE = 1

# Function to send the start message
async def send_start_message(chat_id: int, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Hotel Info", callback_data='hotel-info')],
        [InlineKeyboardButton("Group Info", callback_data='group-info')],
        [InlineKeyboardButton("Today's Menu", callback_data='menu')],
        [InlineKeyboardButton("Flowmaps", callback_data='flowmaps')],
        [InlineKeyboardButton("Point of Contact", callback_data='poc')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text='What would you like to know?', reply_markup=reply_markup)

async def send_welcome_message(update: Update, context: CallbackContext) -> None:
    user_first_name = update.message.from_user.first_name
    welcome_message = (
        f'Jai Swaminarayan {user_first_name}bhai, welcome to your Summer Shibir 2024. '
        'Being your first shibir, I will be here to assist you. You will have a blast.'
    )

    # Path to the local image file
    image_path = 'Assets/SS24Bot.jpg'

    # Check if the image file exists
    if os.path.exists(image_path):
        # Send the message with photo
        with open(image_path, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=photo,
                caption=welcome_message
            )
    else:
        print('could not find file image')

# Command handler for /start
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if (checkExisting(user_id)) == None:
        await send_welcome_message(update, context)
        await asyncio.sleep(2)
        await update.message.reply_text('Please enter your BKMS ID:')
        print('bkms id')
        return ENTER_BKMS_ID
    else:
        await send_start_message(update.message.chat_id, context)

# Callback handler for buttons
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Access user information from query.from_user
    user_first_name = query.from_user.first_name
    user_id = query.from_user.id
    data = checkExisting(user_id)
    bkid = data[0]

    # Handle different button callbacks
    if query.data == 'hotel-info':
        await query.message.reply_text(f'Hotel information for {user_first_name}bhai')


    elif query.data == 'group-info':
        filePath = createGroupImage(bkid)
        welcome_message = (f'Group information for {user_first_name}bhai')
        # Check if the image file exists
        if os.path.exists(filePath):
            # Send the message with photo
            with open(filePath, 'rb') as photo:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=photo,
                    caption=welcome_message
                )
        else:
            print('could not find file image')

    elif query.data == 'menu':
        await query.message.reply_text("Today's Menu is: ...")
    elif query.data == 'flowmaps':
        await query.message.reply_text("Flowmaps")
    elif query.data == 'poc':
        await query.message.reply_text(
        """
Medical Emergencies:
    Primary Contact: Shitalben Patel, RN
    Phone Number: (404) 944-0260

Questions about hotel, transportation, etc:
    Shibir Hotline: (943) 300-7012
        """)

    # Send the start message again
    await asyncio.sleep(2)
    await send_start_message(query.message.chat_id, context) 

# Handler for entering BKMS ID
async def enter_bkms_id(update: Update, context: CallbackContext) -> int:
    bkms_id = update.message.text
    user_id = update.message.from_user.id

    # Example check if BKMS ID matches a certain value (replace with your logic)
    if bkms_id == '1':
        await update.message.reply_text(f'BKMS ID found successfully for {update.message.from_user.first_name}bhai')
        # Write to CSV file
        with open('Data/loginids.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([bkms_id, user_id])
            await send_start_message(update.message.chat_id, context)
    else:
        await update.message.reply_text("BKMS ID not found. Please try again or contact your Group Lead/PC for assistance")
        return ENTER_BKMS_ID

    return ConversationHandler.END

def checkExisting(user_id):
    with open('Data/loginids.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and len(row) >= 2:
                stored_user_id = row[1]
                if stored_user_id == str(user_id):
                    return row
    return


# Command handler for /help
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Help!')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    button_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={},
        fallbacks=[]
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTER_BKMS_ID: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, 
                    enter_bkms_id
                )
            ]
        },
        fallbacks=[]
    )
    # Add handlers to the bot
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)
    application.add_handler(button_handler)  # Add button_handler only once

    scheduler = AsyncIOScheduler()
    scheduler.start()
    application.bot_data['scheduler'] = scheduler

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
