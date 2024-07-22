import logging
import csv
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from tokens import TOKEN
from groupImages import createGroupImage
import pandas as pd
from datetime import datetime, timedelta

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for the conversation handler
ENTER_BKMS_ID = 1

EVENT_START_DATE = datetime(2024, 7, 22)

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

HOTEL_INFORMATION = {
    'Sonesta Gwinnett Place': '1775 Pleasant Hill Rd, Duluth, GA 30096',
    'Best Western Gwinnett': '3670 Shackleford Rd, Duluth, GA 30096',
    'Hampton Inn & Suites': '1725 Pineland Rd Duluth GA 30096'
}

# Read the Excel file
file_path = 'Data/FullData.csv'
df = pd.read_csv(file_path)

# Convert non-numeric values to NaN and drop rows with NaN in 'User ID'
df['User ID'] = pd.to_numeric(df['User ID'], errors='coerce')  # Convert to numeric, invalid parsing will be set as NaN
df = df.dropna(subset=['User ID'])  # Drop rows where 'User ID' is NaN
df['User ID'] = df['User ID'].astype(int)  # Convert the cleaned 'User ID' column to integer

# Convert columns to lists
bkids = df['User ID'].astype(str).tolist()


def get_user_data(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return None  # Return None if user_id is not an integer

    # Retrieve data for the specified user_id
    user_data = df.loc[df["User ID"] == user_id]

    if not user_data.empty:
        # Convert the row of user data to a dictionary
        data = user_data.iloc[0].to_dict()

        # Format birthday if present
        formatted_birthday = data.get("Birthdates", "")
        if formatted_birthday:
            month, day = formatted_birthday.split('/')[0:2]
            data["FormattedBirthday"] = f"{month.zfill(2)}/{day.zfill(2)}"  # Ensure month and day are two digits

        return {
            'User ID': data.get('User ID'),
            'Name': data.get('Name'),
            'Center': data.get('Center'),
            'Registered for Bal Shibir': data.get('Registered for Bal Shibir'),
            'Registered for Kishore Shibir': data.get('Registered for Kishore Shibir'),
            'Group Name': data.get('Group Name'),
            'Bal Group Lead': data.get('Bal Group Lead'),
            'Kishore Group Lead': data.get('Kishore Group Lead'),
            'Birthdates': formatted_birthday,
            'FormattedBirthday': data.get('FormattedBirthday'),
            'Kishore Hotel Name': data.get('Kishore Hotel Name'),
            'Bal Hotel Name': data.get('Bal Hotel Name')
        }
    return None

async def send_start_message(chat_id: int, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Hotel Info", callback_data='hotel-info')],
        [InlineKeyboardButton("Group Info", callback_data='group-info')],
        #[InlineKeyboardButton("Transportation Info", callback_data='transportation-info')],
        [InlineKeyboardButton("Schedule", callback_data='schedule')],
        #[InlineKeyboardButton("Flowmaps", callback_data='flowmaps')],
        [InlineKeyboardButton("Point of Contact", callback_data='poc')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text='What would you like to know?', reply_markup=reply_markup)


async def send_welcome_message(update: Update, context: CallbackContext) -> None:
    user_first_name = update.message.from_user.first_name
    welcome_message = (
        f'Jai Swaminarayan {user_first_name}bhai, welcome to Summer Shibir 2024! We are thrilled to have you join us for this exciting event. Throughout the shibir, you will have the opportunity to connect with fellow participants, engage in various activities, and deepen your understanding of our values and traditions. To make your experience as seamless as possible, I will be here to assist you every step of the way. Get ready for an amazing journey filled with learning, fun, and SAMP.'
    )

    image_path = 'Assets/splashlogo.png'
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

    print('button')

    user_first_name = query.from_user.first_name
    user_id = query.from_user.id
    data = check_existing(user_id)
    if not data or len(data) == 1:
        await query.message.reply_text(f'You are not logged in. Please login with /start')
        return ConversationHandler.END
    bkid = data[0] if data else None

    userdata = get_user_data(bkid)
    name = userdata['Name']
    name = name.split(' ', 1)[0]

    menuButton = True
    global selected_month

    if query.data == 'hotel-info':
        if data[3] == 'bal-shibir':
            hotel = userdata['Bal Hotel Name']
        elif data[3] == 'kishore-shibir':
            hotel = userdata['Kishore Hotel Name']
        else:
            await query.message.reply("Could not get information")
            return ConversationHandler.END
        
        if not hotel or hotel == '':
            await query.message.reply('An error occured')
            return ConversationHandler.END

        address = HOTEL_INFORMATION.get(hotel)
        await query.message.reply_text(f"""
*Hotel Name:* {hotel}
*Hotel Address:* {address}
""", parse_mode='MarkdownV2')
    elif query.data == 'group-info':
        groupName = userdata['Group Name']
        print(groupName, groupName)
        if not type(groupName) == str:
            await query.message.reply_text('You are not in a group!')
            return ConversationHandler.END
        
        print('passed')
        
        if data[3] == 'bal-shibir':
            bal = True
        else:
            bal = False

        kishoreShibir = userdata['Registered for Kishore Shibir']
        print(kishoreShibir, bal, userdata['Bal Group Lead'])
        if kishoreShibir == 'Yes' and bal == True and userdata['Bal Group Lead'] == 'No':
            await query.message.reply_text('You do not have a group for bal shibir')
            return ConversationHandler.END

        names = []

        with open("Data/FullData.csv", mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header row if present

            groupLead = None

            for row in reader:
                # Ensure the row is long enough
                if row[5] == groupName:
                    # Assuming User ID is in column_index 0
                    if row[6] == 'Yes' and bal == True:
                        groupLead = row[1]
                    elif row[7] == 'Yes' and bal == False:
                        groupLead = row[1]
                    names.append(row[1])  # Adjust the index if User ID is in a different column

            file_path = createGroupImage(names, bal, groupName, groupLead)
            group_message = f'Group information for {name}bhai'
            if os.path.exists(file_path):
                with open(file_path, 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        photo=photo,
                        caption=group_message
                    )
            else:
                logger.error('Image file not found.')

    elif query.data == 'transportation-info':
        await query.message.reply_text("Transportation info: ...")
    elif query.data == 'schedule':
        current_date = datetime.now()
        day_diff = (current_date - EVENT_START_DATE).days
        
        if 0 <= day_diff < 8:
            if day_diff == 3:  # Fourth day (0-indexed, so day_diff == 3 is the fourth day)
                if current_date.hour >= 12:
                    image_path = 'Assets/day4schedulebal.png'
                else:
                    image_path = 'Assets/day4schedulekishore.png'
            else:
                image_path = f'Assets/day{day_diff + 1}schedule.png'
            print(image_path)
            if os.path.exists(image_path):
                with open(image_path, 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        caption = f"Today's schedule",
                        photo=photo,
                    )
            else:
                logging.error('Schedule not found')
        else:
            logging.error('Day difference is out of the expected range.')

    elif query.data == 'flowmaps':
        await query.message.reply_text("Flowmaps")
    elif query.data == 'poc':
        message = """
*Medical Emergencies*:
    Primary Contact: Shitalben Patel, RN
    Phone Number: \\(404\\) 944\\-0260

*Non\\-Medical Emergencies*
Questions about hotel, transportation, or if you need directions, etc:
    Shibir Hotline: \\(943\\) 300\\-7012
        """
        await query.message.reply_text(message, parse_mode='MarkdownV2')
    elif query.data == 'bal-shibir':
        await bal_shibir_update(bkid)
        await query.message.reply_text('You will now get information for bal shibir')
    elif query.data == 'kishore-shibir':
        await kishore_shibir_update(bkid)
        await query.message.reply_text('You will now get information for kishore shibir')

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

    return ConversationHandler.END

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

    data = get_user_data(bkms_id)
    name = data['Name']
    name = name.split(' ', 1)[0]

    if bkms_id in bkids:  # Example condition
        await update.message.reply_text(f'BKMS ID found successfully for {name}bhai')
        await asyncio.sleep(1)
        updated_rows = []
        with open('Data/loginids.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and len(row) >= 1:
                    storedbkms = row[0]
                    if storedbkms == bkms_id:
                        row[1] = user_id
                        print('working')
                updated_rows.append(row)

        with open('Data/loginids.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        await birthday_buttons(update)
    else:
        await update.message.reply_text("BKMS ID not found. Please try again or contact your Group Lead/PC for assistance")
        return ENTER_BKMS_ID

    return ConversationHandler.END

async def enter_birthday(month, day, update: Update, context: CallbackContext) -> int:
    MONTHS = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
        'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }

    # Normalize month and day
    month_name = MONTHS.get(month, 'Unknown')
    month_number = month_name.zfill(2)
    day_number = day.zfill(2)

    # Construct the formatted birthday
    birthday = f"{month_number}/{day_number}"

    user_id = update.from_user.id

    data = check_existing(user_id)
    bkid = data[0]

    data = get_user_data(bkid)
    systemBirthday = data['FormattedBirthday']
    if systemBirthday is None:
        await update.message.edit_text('No birthday found for your account.')
        return ConversationHandler.END

    print(systemBirthday, birthday)

    if systemBirthday == birthday:
        await update.message.edit_text('Birthday entered correctly!')
        updated_rows = []
        with open('Data/loginids.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and len(row) >= 2:
                    stored_user_id = row[1]
                    if stored_user_id == str(user_id):
                        row[2] = birthday
                updated_rows.append(row)

        with open('Data/loginids.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        
        await asyncio.sleep(1)

        dataCheck = check_existing(user_id)
        print(dataCheck)
        if not dataCheck[3] == '':
            return await send_start_message(update.message.chat_id, context)

        if data['Registered for Bal Shibir'] == "Yes" and data['Registered for Kishore Shibir'] == 'Yes':
            print('registered for both')
            keyboard = [
            [InlineKeyboardButton("Bal Shibir", callback_data='bal-shibir')],
            [InlineKeyboardButton("Kishore Shibir", callback_data='kishore-shibir')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(text='You are registered for both bal and kishore shibir. Which shibir do you want information for?', reply_markup=reply_markup)
        elif data['Registered for Bal Shibir'] == 'Yes':
            updated_rows = []
            with open('Data/loginids.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) >= 1:
                        storedbkms = row[0]
                        if storedbkms == bkid:
                            row[3] = 'kishore-shibir'
                            print('working')
                    updated_rows.append(row)

            with open('Data/loginids.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
                await update.message.reply_text(text='Jai Swaminarayan, you are registered for bal shibir. Please use the menu below to get information for it.')
                await bal_shibir_update(bkid)
                await send_start_message(update.message.chat_id, context)
        elif data['Registered for Kishore Shibir'] == 'Yes':
            await update.message.reply_text(text='Jai Swaminarayan, you are registered for kishore shibir. Please use the menu below to get information for it.')
            await kishore_shibir_update(bkid)
            await send_start_message(update.message.chat_id, context)
        else:
            await update.message.reply_text(text='You are not registered for either bal or kishore shibir. Thank you for using this bot!')
    else:
        await update.message.edit_text('Please enter the birthday associated with your BKMS account')

    return ConversationHandler.END

def check_existing(user_id):
    with open('Data/loginids.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:  # Check if the row has at least 2 elements
                stored_user_id = row[1]
                if stored_user_id == str(user_id):
                    return row
    return None


async def change_id(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    found = False
    updated_rows = []
    
    # Read the CSV file and process each row
    with open('Data/loginids.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1 and row[1] == str(user_id):
                # If this row contains the user_id, modify the row
                row[1] = ''  # Clear the user_id field
                row[2] = ''  # Clear the birthday field
                row[3] = '' # Clear the shibir field
                found = True
            updated_rows.append(row)

    # Write the updated rows back to the CSV file
    with open('Data/loginids.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    if found:
        await update.message.reply_text('Logged out of your BKMS. Run /start to login with another id')
    else:
        await update.message.reply_text('Could not find ID. Please login using /start first.')
    
async def change_shibir(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    updated_rows = []
    found = False

    with open('Data/loginids.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and len(row) > 1 and row[1] == str(user_id):
                found = True
                data = check_existing(user_id)
                bkid = data[0]
                moreData = get_user_data(bkid)

                if moreData['Registered for Bal Shibir'] == 'Yes' and moreData['Registered for Kishore Shibir'] == 'Yes':
                    if len(row) > 3:
                        if row[3] == 'bal-shibir':
                            row[3] = 'kishore-shibir'
                            await update.message.reply_text('You will now get information for Kishore Shibir')
                        elif row[3] == 'kishore-shibir':
                            row[3] = 'bal-shibir'
                            await update.message.reply_text('You will now get information for Bal Shibir')
                        else:
                            row[3] = 'kishore-shibir'
                            await update.message.reply_text('You will now get information for Kishore Shibir')
                    else:
                        # Handle case where the row does not have enough columns
                        row[3] = 'kishore-shibir'  # Default value if index 3 is not present
                        await update.message.reply_text('You will now get information for Kishore Shibir')
                else:
                    if moreData['Registered for Bal Shibir'] == 'Yes':
                        await update.message.reply_text('You are only registered for Bal Shibir!')
                    elif moreData['Registered for Kishore Shibir'] == 'Yes':
                        await update.message.reply_text('You are only registered for Kishore Shibir!')
            updated_rows.append(row)
    
    if found:
        with open('Data/loginids.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
    else:
        await update.message.reply_text('User ID not found. Please login using /start first')

    

async def bal_shibir_update(bkid):
    updated_rows = []
    with open('Data/loginids.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and len(row) >= 1:
                storedbkms = row[0]
                if storedbkms == bkid:
                    row[3] = 'bal-shibir'
            updated_rows.append(row)

    with open('Data/loginids.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

async def kishore_shibir_update(bkid):
    updated_rows = []
    with open('Data/loginids.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and len(row) >= 1:
                storedbkms = row[0]
                if storedbkms == bkid:
                    row[3] = 'kishore-shibir'
            updated_rows.append(row)

    with open('Data/loginids.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)


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

    application.add_handler(CommandHandler("change_id", change_id))
    application.add_handler(CommandHandler("change_shibir", change_shibir))
    application.add_handler(conv_handler)
    application.add_handler(button_handler)


    application.run_polling()

if __name__ == '__main__':
    main()
