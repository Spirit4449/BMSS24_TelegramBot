import logging
import csv
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tokens import TOKEN
from groupImages import createGroupImage

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for the conversation handler
ENTER_BKMS_ID = 1

MONTHS = [
    {"name": "January", "days": list(range(1, 32))},
    {"name": "February", "days": list(range(1, 29))},  # Simplified feor the example
    {"name": "March", "days": list(range(1, 32))},
    {"name": "April", "days": list(range(1, 31))},
    {"name": "May", "days": list(range(1, 32))},
    {"name": "June", "days": list(range(1, 31))},
    {"name": "July", "days": list(range(1, 32))},
    {"name": "August", "days": list(range(1, 32))},
    {"name": "September", "days": list(range(1, 31))},
    {"name": "October", "days": list(range(1, 32))},
    {"name": "November", "days": list(range(1, 31))},
    {"name": "December", "days": list(range(1, 32))}
]

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

    image_path = 'Assets/SS24Bot.jpg'
    if os.path.exists(image_path):
        with open(image_path, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=photo,
                caption=welcome_message
            )
    else:
        logger.error('Image file not found.')

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    print(user_id)
    data = check_existing(user_id)
    if not data or len(data) == 1:
        await send_welcome_message(update, context)
        await asyncio.sleep(2)
        await update.message.reply_text('Please enter your BKMS ID:')
        return ENTER_BKMS_ID
    else:
        await send_start_message(update.message.chat_id, context)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    user_first_name = query.from_user.first_name
    user_id = query.from_user.id
    data = check_existing(user_id)
    bkid = data[0] if data else None

    menuButton = True
    global selected_month


    if query.data == 'hotel-info':
        await query.message.reply_text(f'Hotel information for {user_first_name}bhai')

    elif query.data == 'group-info':
        file_path = createGroupImage(bkid)
        group_message = f'Group information for {user_first_name}bhai'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as photo:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=photo,
                    caption=group_message
                )
        else:
            logger.error('Image file not found.')

    elif query.data == 'menu':
        await query.message.reply_text("Today's Menu is: ...")
    elif query.data == 'flowmaps':
        await query.message.reply_text("Flowmaps")
    elif query.data == 'poc':
        message = """
*Medical Emergencies*:
    Primary Contact: Shitalben Patel, RN
    Phone Number: \(404\) 944\-0260

*Non\-Medical Emergencies*
Questions about hotel, transportation, or if you need directions, etc:
    Shibir Hotline: \(943\) 300\-7012
        """
        await query.message.reply_text(message, parse_mode='MarkdownV2')
    elif any(month["name"] == query.data for month in MONTHS):
        selected_month = next((month for month in MONTHS if month["name"] == query.data), None)
        if selected_month:
            menuButton = False
            await update_days_keyboard(query)
    elif query.data.isdigit() and selected_month:
        menuButton = False
        selected_day = int(query.data)
        month_str = selected_month["name"]
        day_str = str(selected_day)
        
        await enter_birthday(month_str, day_str, query, context)


    if 'delayed_task' in context.user_data:
        context.user_data['delayed_task'].cancel()
    if menuButton == True:
        context.user_data['delayed_task'] = asyncio.create_task(delayed_start_message(query.message.chat_id, context))

async def update_days_keyboard(query):
    global selected_month

    if selected_month:
        days_range = selected_month["days"]
        days_buttons = [InlineKeyboardButton(str(day), callback_data=str(day)) for day in days_range]
        days_keyboard = [days_buttons[i:i+7] for i in range(0, len(days_buttons), 7)]
        reply_markup = InlineKeyboardMarkup(days_keyboard)

        await query.message.edit_text(f'You selected {selected_month["name"]}. Please select your birth day:', reply_markup=reply_markup)
    else:
        await query.message.reply_text("Please select a month first.")

async def delayed_start_message(chat_id: int, context: CallbackContext) -> None:
    await asyncio.sleep(2.5)
    await send_start_message(chat_id, context)

async def birthday_buttons(query):
    keyboard = [
       [InlineKeyboardButton(month["name"], callback_data=month["name"]) for month in row] for row in chunked_months(MONTHS, 3)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(text='Enter your birthday to access this information. You only have to do this once.', reply_markup=reply_markup)

def chunked_months(months, size):
    return [months[i:i + size] for i in range(0, len(months), size)]

async def enter_bkms_id(update: Update, context: CallbackContext) -> int:
    bkms_id = update.message.text
    user_id = update.message.from_user.id

    if bkms_id == '1':  # Example condition
        await update.message.reply_text(f'BKMS ID found successfully for {update.message.from_user.first_name}bhai')
        with open('Data/loginids.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([bkms_id, user_id])
            await birthday_buttons(update)
    else:
        await update.message.reply_text("BKMS ID not found. Please try again or contact your Group Lead/PC for assistance")
        return ENTER_BKMS_ID

    return ConversationHandler.END

async def enter_birthday(month, day, update: Update, context: CallbackContext) -> int:
    print(month, day)
    birthday = '1'
    user_id = update.from_user.id

    if birthday == '1':  # Example condition
        await update.message.edit_text(f'Birthday entered successfully')
        updated_rows = []
        with open('Data/loginids.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and len(row) >= 2:
                    stored_user_id = row[1]
                    print(stored_user_id, user_id)
                    if stored_user_id == str(user_id):
                        print('matching')
                        row.append(birthday)
                updated_rows.append(row)

        with open('Data/loginids.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        
        await asyncio.sleep(1)
        await send_start_message(update.message.chat_id, context)
    else:
        await update.message.edit_text("Birthday is incorrect. Please try again or contact Group Lead/PC for assistance.")

    return ConversationHandler.END

def check_existing(user_id):
    with open('Data/loginids.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            stored_user_id = row[1]
            if stored_user_id == str(user_id):
                return row
    return None

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

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)
    application.add_handler(button_handler)

    scheduler = AsyncIOScheduler()
    scheduler.start()
    application.bot_data['scheduler'] = scheduler

    application.run_polling()

if __name__ == '__main__':
    main()
