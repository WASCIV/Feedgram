import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot_creator_id = 645325762  # Replace with your Telegram ID
bot_token = 'YOUR_TOKEN'  # Replace with your bot token

user_chats = {}


def start(update, context):
    update.message.reply_text('Hi! How can I help you?')


def feedback(update, context):
    chat_id = update.message.chat_id

    if chat_id != bot_creator_id:
        username = update.message.from_user.username
        username = f'@{username}' if username else 'No username'

        if update.message.text:
            user_chats[chat_id] = update.message.text
            bot_message = f"User {chat_id} ({username}): {update.message.text}"
            update.message.reply_text('Thanks for your feedback! I will get back to you as soon as possible. This Bot is Open Source Check This ')
            context.bot.send_message(chat_id=bot_creator_id, text=bot_message)

        if update.message.photo or update.message.video or update.message.document:
            context.bot.forward_message(chat_id=bot_creator_id, from_chat_id=chat_id, message_id=update.message.message_id)

        print('User Chat ID:', chat_id)
        print('User Message:', update.message.text)

    elif chat_id == bot_creator_id:
        if update.message.text:
            try:
                reply_chat_id, reply_message = update.message.text.split(" ", 1)
                reply_chat_id = int(reply_chat_id)
                if reply_chat_id in user_chats:
                    context.bot.send_message(chat_id=reply_chat_id, text=reply_message)
                    print('Bot Reply:', reply_message)
                else:
                    context.bot.send_message(chat_id=bot_creator_id, text='Invalid chat ID.')
                    print('Error: Invalid chat ID')
            except ValueError:
                context.bot.send_message(chat_id=bot_creator_id, text='Incorrect format: Use "chat_id message".')
                print('Error: Incorrect format')

        if update.message.caption:
            try:
                reply_chat_id, reply_caption = update.message.caption.split(" ", 1)
                reply_chat_id = int(reply_chat_id)
                if reply_chat_id in user_chats:
                    if update.message.photo:
                        context.bot.send_photo(chat_id=reply_chat_id, photo=update.message.photo[-1].file_id, caption=reply_caption)
                    elif update.message.video:
                        context.bot.send_video(chat_id=reply_chat_id, video=update.message.video.file_id, caption=reply_caption)
                    elif update.message.document:
                        context.bot.send_document(chat_id=reply_chat_id, document=update.message.document.file_id, caption=reply_caption)
                else:
                    context.bot.send_message(chat_id=bot_creator_id, text='Invalid chat ID.')
                    print('Error: Invalid chat ID')
            except ValueError:
                context.bot.send_message(chat_id=bot_creator_id, text='Incorrect format: Use "chat_id description" as the caption.')
                print('Error: Incorrect format')


def main():
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, feedback))
    dp.add_handler(MessageHandler(Filters.photo | Filters.video | Filters.document, feedback))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
