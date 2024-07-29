# Summer Shibir 2024 Telegram Bot

Welcome to the BMSS24 Telegram Bot project! This bot is designed to manage and interact with participants of the BMSS24 event, providing a seamless and engaging experience.
You can access the bot using this link: https://t.me/BMSS24_bot

## Description
The Summer Shibir 2024 Telegram Bot is a Python-based bot that helps automate various tasks for the BMSS24 event. The bot uses the `python-telegram-bot` library to interact with the Telegram API. It is hosted on AWS EC2 so it can be online 24/7

## Features

- **Hotel Information**: View what hotel you are staying at and the address of it
- **Group Information**: View group name, participants, and the group lead
- **Schedule**: View the day's schedule
- **Menu**: Get the day's menu including breakfast, lunch, snack, dinner, and desert
- **Emergency Contact**: Get a list of phone numbers for emergency contact including a hotline number

## Installation
How to install

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/BMSS24-Telegram-Bot.git
   cd BMSS24-Telegram-Bot

 2. **Create a virtual environment**:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

 4. **Enter the bots token**:
    Create a `tokens.py` file and enter the following code. Replace `YOUR_TOKEN_HERE` with the acutal token of your bot
     ```sh
     TOKEN='YOUR_TOKEN_HERE'
     ```
5. **Run the bot**:
    ```sh
    python main.py
    ```




This bot is only to be used for BAPS events. If you have any questions please reach out to me at nischayp510@gmail.com
