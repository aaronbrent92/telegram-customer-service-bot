import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("7835775405:AAH62Y3AfzFeNwQLslApSL8WAXbmUiAYp50")
CHANNEL_USERNAME = os.getenv("@BHTCLUBVIPOFFICIAL")

gift_codes = {"FREE2025", "HELLOAI", "WELCOME123"}

async def is_user_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_user_subscribed(user_id, context):
        await update.message.reply_text(f"🚫 You must subscribe to our channel first:\n{CHANNEL_USERNAME}")
        return

    keyboard = [
        [InlineKeyboardButton("🎁 Gift Code", callback_data='gift')],
        [InlineKeyboardButton("🔮 Prediction Channel", url="https://t.me/BHTCLUBVIPOFFICIAL")],
        [InlineKeyboardButton("💰 Deposit Issue", callback_data='deposit')],
        [InlineKeyboardButton("🏦 Withdraw Issue", callback_data='withdraw')],
    ]
    await update.message.reply_text("✅ Welcome! Choose an option:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['state'] = query.data

    if query.data == 'gift':
        await query.edit_message_text("🎁 Enter your gift code:")
    elif query.data == 'deposit':
        await query.edit_message_text("💰 Please describe your deposit issue:")
    elif query.data == 'withdraw':
        await query.edit_message_text("🏦 Please describe your withdrawal issue:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    state = context.user_data.get('state')

    if state == 'gift':
        if message in gift_codes:
            gift_codes.remove(message)
            await update.message.reply_text("✅ Gift code accepted! You've received your reward.")
        else:
            await update.message.reply_text("❌ Invalid or already used gift code.")
    elif state in ['deposit', 'withdraw']:
        await update.message.reply_text("✅ Thank you! Our team will contact you shortly.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
