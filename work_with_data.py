from telegram.ext import Updater, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, bot
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import Updater, MessageHandler, Filters


BOT_TOKEN = ''


def downloader(update, context):
    context.bot.get_file(update.message.document).download()

    # writing to a custom file
    with open("file_0.pdf", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)


updater = Updater(BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(MessageHandler(Filters.document, downloader))

updater.start_polling()
updater.idle()

