# 🏋️ FitClub Telegram Bot

A feature-rich Telegram bot for fitness clubs to manage class schedules, bookings, and member inquiries.

## ✨ Features

- **Class Schedule**: View daily fitness class schedules with times, durations, and instructors
- **Book Classes**: Interactive booking system with class selection and time slot choices
- **My Bookings**: Track your personal booking history
- **Club Information**: Get details about facilities, hours, and membership options
- **Contact Info**: Quick access to club contact details
- **Interactive Menu**: User-friendly inline keyboard navigation
- **Help System**: Comprehensive help commands

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/menu` | Display main menu with all options |
| `/help` | Show help information |
| `/schedule` | View today's class schedule |
| `/book` | Book a fitness class |
| `/mybookings` | View your booking history |
| `/info` | Get club information |
| `/contact` | View contact details |
| `/cancel` | Cancel current operation |

## 🚀 Installation Guide

### Prerequisites

- Python 3.7 or higher
- A Telegram account
- Git (optional, for cloning)

### Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat with BotFather and send `/newbot`
3. Follow the instructions:
   - Choose a name for your bot (e.g., "FitClub Bot")
   - Choose a username for your bot (must end in 'bot', e.g., "fitclub_test_bot")
4. BotFather will give you a **BOT TOKEN** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. **Save this token** - you'll need it in the next steps!

### Step 2: Clone or Download the Bot

```bash
# Navigate to your workspace
cd /workspace

# The bot file is already created: fitness_bot.py
```

### Step 3: Install Dependencies

```bash
# Install the python-telegram-bot library
pip install python-telegram-bot
```

### Step 4: Set Up Environment Variable

#### On Linux/Mac:
```bash
export TELEGRAM_BOT_TOKEN='YOUR_BOT_TOKEN_HERE'
```

#### On Windows (Command Prompt):
```cmd
set TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

#### On Windows (PowerShell):
```powershell
$env:TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
```

**Replace `YOUR_BOT_TOKEN_HERE` with the token you got from BotFather.**

### Step 5: Run the Bot

```bash
python fitness_bot.py
```

You should see:
```
🤖 FitClub Bot is running... Press Ctrl+C to stop.
```

### Step 6: Test Your Bot

1. Open Telegram
2. Search for your bot by username (e.g., @fitclub_test_bot)
3. Click **Start** or send `/start`
4. Try the different commands:
   - `/menu` - See the main menu
   - `/schedule` - View class schedule
   - `/book` - Book a class
   - `/help` - Get help

## 📁 Project Structure

```
/workspace/
├── fitness_bot.py      # Main bot code
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## 🔧 Configuration

The bot uses the following environment variable:

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather | Yes |

## 🎯 How It Works

### Booking Flow:
1. User sends `/book` or clicks "Book Class"
2. Selects a fitness class (Yoga, Pilates, CrossFit, etc.)
3. Chooses a time slot
4. Confirms the booking
5. Receives confirmation with booking details

### Data Storage:
- Currently uses in-memory storage (for testing)
- Bookings are stored in a dictionary (`user_bookings`)
- **Note**: Data will be lost when the bot restarts
- For production, integrate with a database (SQLite, PostgreSQL, etc.)

## 🛠️ Customization

### Modify Fitness Classes

Edit the `FITNESS_CLASSES` dictionary in `fitness_bot.py`:

```python
FITNESS_CLASSES = {
    "yoga": {"name": "Yoga Session", "duration": "60 min", "instructor": "Sarah"},
    "pilates": {"name": "Pilates", "duration": "45 min", "instructor": "Mike"},
    # Add your own classes here
}
```

### Update Club Information

Modify the `show_club_info()` function to update:
- Address
- Opening hours
- Facilities
- Membership options

### Change Contact Details

Update the `show_contact()` function with your actual:
- Email
- Phone number
- Website
- Social media handles

## 🐛 Troubleshooting

### Bot doesn't start
- Check if `TELEGRAM_BOT_TOKEN` is set correctly
- Verify the token is valid (no extra spaces or quotes)
- Ensure Python 3.7+ is installed

### Can't find my bot in Telegram
- Make sure you completed the setup with @BotFather
- Try searching by the exact username (including the 'bot' suffix)
- The bot must be started at least once before it appears in searches

### Commands not working
- Type commands exactly as shown (case-sensitive)
- Use `/help` to see available commands
- Restart the bot if issues persist

### Module not found error
```bash
# Reinstall the telegram library
pip install --upgrade python-telegram-bot
```

## 📝 Development Tips

### Run in background (Linux/Mac):
```bash
nohup python fitness_bot.py &
```

### View logs:
The bot outputs logs to console. For file logging, modify the `logging.basicConfig` section.

### Stop the bot:
Press `Ctrl+C` in the terminal where it's running.

## 🔐 Security Notes

- **Never commit your bot token to version control**
- Keep your token secret
- For production, use environment variables or a secrets manager
- Consider adding user authentication for real bookings

## 🚀 Next Steps for Production

1. **Database Integration**: Replace in-memory storage with SQLite/PostgreSQL
2. **User Authentication**: Add login/registration system
3. **Payment Integration**: Connect payment gateways for memberships
4. **Admin Panel**: Create admin commands for managing bookings
5. **Notifications**: Send reminder messages before classes
6. **Deploy**: Host on a server (Heroku, AWS, DigitalOcean, etc.)

## 📄 License

This project is open source and available for modification.

## 💬 Support

For questions or issues:
- Check the `/help` command in the bot
- Review the troubleshooting section above
- Modify the contact information in the code for your support channel

---

**Enjoy using FitClub Bot! 🏋️💪**
