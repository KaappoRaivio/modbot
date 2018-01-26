#
#
# import logging
# from telegram.ext import *
#
# updater = Updater(token='525786228:AAHE36X67LKReTNYYwQ4wZQ6VhlVK94Hwk8')
# dispatcher = updater.dispatcher
#
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# def start(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text='testi')
# def echo(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
#
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
# echo_handler = MessageHandler(Filters.text, echo)
# dispatcher.add_handler(echo_handler)
#
# updater.start_polling()
