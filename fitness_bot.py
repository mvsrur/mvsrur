#!/usr/bin/env python3
"""
Fitness Club Telegram Bot
A bot for managing fitness club memberships, schedules, and inquiries.
"""

import os
import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
SELECTING_ACTION, SELECTING_CLASS, BOOKING_CONFIRM = range(3)

# Mock data for fitness classes
FITNESS_CLASSES = {
    "yoga": {"name": "Yoga Session", "duration": "60 min", "instructor": "Sarah"},
    "pilates": {"name": "Pilates", "duration": "45 min", "instructor": "Mike"},
    "crossfit": {"name": "CrossFit", "duration": "60 min", "instructor": "John"},
    "zumba": {"name": "Zumba", "duration": "50 min", "instructor": "Maria"},
    "spinning": {"name": "Spinning", "duration": "45 min", "instructor": "Alex"},
}

# Mock user database (in production, use a real database)
user_bookings = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"🏋️ Welcome to FitClub Bot, {user.first_name}!\n\n"
        "I can help you with:\n"
        "• View class schedule\n"
        "• Book a class\n"
        "• Check your bookings\n"
        "• Club information\n"
        "• Contact us\n\n"
        "Use /menu to see available options or type /help for more info."
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "📚 *FitClub Bot Help*\n\n"
        "*Available Commands:*\n"
        "/start - Start the bot\n"
        "/menu - Show main menu\n"
        "/schedule - View class schedule\n"
        "/book - Book a class\n"
        "/mybookings - View your bookings\n"
        "/info - Club information\n"
        "/contact - Contact information\n"
        "/cancel - Cancel current operation\n\n"
        "*How to book a class:*\n"
        "1. Use /book command\n"
        "2. Select your preferred class\n"
        "3. Choose a time slot\n"
        "4. Confirm your booking\n\n"
        "Need more help? Contact us at info@fitclub.com"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display main menu."""
    keyboard = [
        [
            InlineKeyboardButton("📅 View Schedule", callback_data="schedule"),
            InlineKeyboardButton("📝 Book Class", callback_data="book"),
        ],
        [
            InlineKeyboardButton("📋 My Bookings", callback_data="mybookings"),
            InlineKeyboardButton("ℹ️ Club Info", callback_data="info"),
        ],
        [
            InlineKeyboardButton("📞 Contact", callback_data="contact"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏋️ What would you like to do?",
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks from inline keyboards."""
    query = update.callback_query
    await query.answer()
    
    action = query.data
    
    if action == "schedule":
        await show_schedule(update, context)
    elif action == "book":
        await start_booking(update, context)
    elif action == "mybookings":
        await show_my_bookings(update, context)
    elif action == "info":
        await show_club_info(update, context)
    elif action == "contact":
        await show_contact(update, context)
    elif action.startswith("class_"):
        class_type = action.replace("class_", "")
        await select_time_slot(update, context, class_type)
    elif action.startswith("time_"):
        time_slot = action.replace("time_", "")
        await confirm_booking(update, context, time_slot)
    elif action == "confirm_yes":
        await finalize_booking(update, context)
    elif action == "confirm_no":
        await cancel_booking(update, context)


async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display class schedule."""
    schedule_text = "📅 *Today's Class Schedule*\n\n"
    
    # Generate schedule for today
    base_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    for i, (class_key, class_info) in enumerate(FITNESS_CLASSES.items()):
        class_time = base_time + timedelta(hours=i)
        schedule_text += (
            f"*{class_time.strftime('%H:%M')}* - {class_info['name']}\n"
            f"  Duration: {class_info['duration']} | Instructor: {class_info['instructor']}\n\n"
        )
    
    keyboard = [[InlineKeyboardButton("📝 Book Now", callback_data="book")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            schedule_text, 
            reply_markup=reply_markup, 
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            schedule_text, 
            reply_markup=reply_markup, 
            parse_mode='Markdown'
        )


async def start_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the booking process."""
    keyboard = []
    for class_key, class_info in FITNESS_CLASSES.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{class_info['name']} ({class_info['duration']})", 
                callback_data=f"class_{class_key}"
            )
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "📝 Select a class to book:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "📝 Select a class to book:",
            reply_markup=reply_markup
        )
    
    return SELECTING_CLASS


async def select_time_slot(update: Update, context: ContextTypes.DEFAULT_TYPE, class_type: str):
    """Show available time slots for selected class."""
    context.user_data['selected_class'] = class_type
    
    # Generate time slots
    base_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    slots = []
    
    for i in range(6):
        slot_time = base_time + timedelta(hours=i)
        slots.append(slot_time.strftime("%H:%M"))
    
    keyboard = []
    for slot in slots:
        keyboard.append([
            InlineKeyboardButton(slot, callback_data=f"time_{slot}")
        ])
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    class_name = FITNESS_CLASSES[class_type]['name']
    await update.callback_query.edit_message_text(
        f"You selected: *{class_name}*\n\nChoose a time slot:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return SELECTING_CLASS


async def confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE, time_slot: str):
    """Confirm booking details."""
    context.user_data['selected_time'] = time_slot
    
    class_type = context.user_data.get('selected_class')
    class_name = FITNESS_CLASSES[class_type]['name']
    
    confirmation_text = (
        "Please confirm your booking:\n\n"
        f"📋 *Class:* {class_name}\n"
        f"⏰ *Time:* {time_slot}\n"
        f"📅 *Date:* {datetime.now().strftime('%Y-%m-%d')}\n\n"
        "Do you want to proceed?"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes", callback_data="confirm_yes"),
            InlineKeyboardButton("❌ No", callback_data="confirm_no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        confirmation_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return BOOKING_CONFIRM


async def finalize_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finalize the booking."""
    user_id = update.effective_user.id
    class_type = context.user_data.get('selected_class')
    time_slot = context.user_data.get('selected_time')
    class_name = FITNESS_CLASSES[class_type]['name']
    
    # Store booking
    if user_id not in user_bookings:
        user_bookings[user_id] = []
    
    booking = {
        'class': class_name,
        'time': time_slot,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'timestamp': datetime.now()
    }
    user_bookings[user_id].append(booking)
    
    success_message = (
        "✅ *Booking Confirmed!*\n\n"
        f"📋 Class: {class_name}\n"
        f"⏰ Time: {time_slot}\n"
        f"📅 Date: {booking['date']}\n\n"
        "We look forward to seeing you!\n"
        "Use /mybookings to view your bookings."
    )
    
    keyboard = [[InlineKeyboardButton("📋 View My Bookings", callback_data="mybookings")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        success_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    # Clear user data
    context.user_data.clear()
    
    return ConversationHandler.END


async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the booking process."""
    context.user_data.clear()
    
    await update.callback_query.edit_message_text("Booking cancelled. Use /menu to start over.")
    
    return ConversationHandler.END


async def show_my_bookings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's bookings."""
    user_id = update.effective_user.id
    
    if user_id not in user_bookings or not user_bookings[user_id]:
        message = "You don't have any bookings yet.\nUse /book to book a class!"
    else:
        message = "📋 *Your Bookings:*\n\n"
        for i, booking in enumerate(user_bookings[user_id][-5:], 1):  # Show last 5 bookings
            message += (
                f"{i}. *{booking['class']}*\n"
                f"   📅 {booking['date']} at {booking['time']}\n\n"
            )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text(message, parse_mode='Markdown')


async def show_club_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show club information."""
    info_text = (
        "🏋️ *FitClub Information*\n\n"
        "📍 *Address:*\n"
        "123 Fitness Street\n"
        "Health City, HC 12345\n\n"
        "⏰ *Opening Hours:*\n"
        "Monday - Friday: 6:00 AM - 10:00 PM\n"
        "Saturday: 8:00 AM - 8:00 PM\n"
        "Sunday: 9:00 AM - 6:00 PM\n\n"
        "💪 *Facilities:*\n"
        "• Modern gym equipment\n"
        "• Group fitness studios\n"
        "• Personal training\n"
        "• Locker rooms & showers\n"
        "• Free WiFi\n"
        "• Parking available\n\n"
        "🎯 *Membership Options:*\n"
        "• Day Pass: $15\n"
        "• Monthly: $50\n"
        "• Annual: $500 (Save 17%!)"
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(info_text, parse_mode='Markdown')
    else:
        await update.message.reply_text(info_text, parse_mode='Markdown')


async def show_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show contact information."""
    contact_text = (
        "📞 *Contact Us*\n\n"
        "📧 Email: info@fitclub.com\n"
        "📱 Phone: +1 (555) 123-4567\n"
        "🌐 Website: www.fitclub.com\n\n"
        "📱 *Social Media:*\n"
        "Instagram: @fitclub_official\n"
        "Facebook: /fitclub\n"
        "Twitter: @fitclub\n\n"
        "💬 For immediate assistance, call us during opening hours."
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(contact_text, parse_mode='Markdown')
    else:
        await update.message.reply_text(contact_text, parse_mode='Markdown')


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel current operation."""
    context.user_data.clear()
    await update.message.reply_text("Operation cancelled. Use /menu to start over.")
    return ConversationHandler.END


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text(
        "Sorry, I didn't understand that command. Use /help to see available commands."
    )


def main() -> None:
    """Start the bot."""
    # Get the bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Please set it with: export TELEGRAM_BOT_TOKEN='your_bot_token'")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Set up conversation handler for booking
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('book', start_booking),
            CallbackQueryHandler(button_callback, pattern='^(book)$'),
        ],
        states={
            SELECTING_ACTION: [
                CallbackQueryHandler(button_callback),
            ],
            SELECTING_CLASS: [
                CallbackQueryHandler(button_callback),
            ],
            BOOKING_CONFIRM: [
                CallbackQueryHandler(button_callback),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)],
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("schedule", show_schedule))
    application.add_handler(CommandHandler("mybookings", show_my_bookings))
    application.add_handler(CommandHandler("info", show_club_info))
    application.add_handler(CommandHandler("contact", show_contact))
    application.add_handler(CommandHandler("cancel", cancel_command))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    # Start the Bot
    logger.info("Bot started successfully!")
    print("🤖 FitClub Bot is running... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
