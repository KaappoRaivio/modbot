# #
# #
# # import logging
# # from telegram.ext import *
# #
# # updater = Updater(token='525786228:AAHE36X67LKReTNYYwQ4wZQ6VhlVK94Hwk8')
# # dispatcher = updater.dispatcher
# #
# # logging.basicConfig(level=logging.DEBUG,
# #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# #
# # def start(bot, update):
# #     bot.send_message(chat_id=update.message.chat_id, text='testi')
# # def echo(bot, update):
# #     bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
# #
# # start_handler = CommandHandler('start', start)
# # dispatcher.add_handler(start_handler)
# # echo_handler = MessageHandler(Filters.text, echo)
# # dispatcher.add_handler(echo_handler)
# #
# # # updater.start_polling()
#
# # import sys
# # import time
# # import telepot
# # from telepot.loop import MessageLoop
# #
# # def handle(msg):
# #     content_type, chat_type, chat_id = telepot.glance(msg)
# #     print(content_type, chat_type, chat_id)
# #
# #     if content_type == 'text':
# #         bot.sendMessage(chat_id, msg['text'])
# #
# # TOKEN = sys.argv[1]  # get token from command-line
# #
# # bot = telepot.Bot(TOKEN)
# # MessageLoop(bot, handle).run_as_thread()
# # print ('Listening ...')
# #
# # # Keep the program running.
# # while 1:
# #     time.sleep(10)
#
# import sys
# import time
# import telepot
# from telepot.loop import MessageLoop
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
#
# def on_chat_message(msg):
#     content_type, chat_type, chat_id = telepot.glance(msg)
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#                    [InlineKeyboardButton(text='Press me', callback_data='press')],
#                ])
#
#     bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)
#
# def on_callback_query(msg):
#     query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
#     print('Callback Query:', query_id, from_id, query_data)
#
#     bot.answerCallbackQuery(query_id, text='Got it')
#
# TOKEN = sys.argv[1]  # get token from command-line
#
# bot = telepot.Bot(TOKEN)
# MessageLoop(bot, {'chat': on_chat_message,
#                   'callback_query': on_callback_query}).run_as_thread()
# print('Listening ...')
#
# while 1:
#     time.sleep(10)

import json
import requests
import wget
from watson_developer_cloud import NaturalLanguageClassifierV1, VisualRecognitionV3
import telegram
import urllib


# Authentication stuff
telegram_bot_token = ''
watson_v_r_token = ''
watson_nlc_password = ''
watson_nlc_username = ''
watson_nlc_id = ''

lxybot = telegram.Bot(telegram_bot_token)  # initializing a telegram bot instance.
URL = "https://api.telegram.org/bot{}/".format(telegram_bot_token)  # the base URL of the bot api.


def visual_recognition(path):
    """
    Desc:
        Returns, whether or not a given input is a picture about a black board.
    Takes:
        str path    : A string containing the path to the image that is going to be classified.
    Returns:
        str thingy  : whether a string containing 'liitutaulu' or 'epäliitutaulu', depending the outcome of the Visual Recognition service.
    Note:
        None
    Raises:
        None
    """
    def getHighestClass(response):
        """
        Desc:
            Returns the class with highest score from the JSON object that the parent funtion returns.
        Takes:
            JSON response   : the JSON object that the parent function returns.
        Returns:
            float   : The highest score out of the classes.
        Note:
            Works only with the parent function; nothing else.
        Raises:
            None.
        """
        response = response['images'][0]['classifiers'][0]['classes']
        classes, scores = [], []
        for i in response:
            classes.append(i['class'])
            scores.append(i['score'])
        if response[0]['score'] > response[1]['score']:
            print(response[0]['class'])
            return response[0]['class']
        else:
            print(response[1]['class'])
            return response[1]['class']
    visual_recognition = VisualRecognitionV3('2016-05-20', api_key=watson_v_r_token)
    response = visual_recognition.classify(images_file=open(path, 'rb'), threshold=0, classifier_ids=['Liitutauluvaiei_518054255'])
    thingy = getHighestClass(response)
    return thingy


def watson(text):  # This function determines, which school subject is being talked about in the input string.
    """
    Desc:
        An IBM Watson Natural Language Classifier instance, that determines, what school subjet is being talked about.
    Takes:
        str text        : The input string that the function classifies.
    Returns:
        str top_class   : The school subject with the highest confidence.
        IF the confidence is under the certain point, it returns only
        none None
    Notes:
        None
    Raises:
        None
    """
    def getTopClassConfidence(top_class, response):
        """
        Desc:
            Returns the confidence of the parent funtion's top_class str.
        Takes:
            str top_class   : The class with the highes confidence; See the desc of the parent function.
            JSON response   : The JSON object representing the response from the IBM NLC.
        Retunrs:
            float confidence    : The confidence of the top class.
        Note:
            Only works together with the parent funcntion.
        Raises:
            None
        """
        for i in response['classes']:
            if i['class_name'] == top_class:
                return i['confidence']

    natural_language_classifier = NaturalLanguageClassifierV1(
        username=watson_nlc_username,
        password=watson_nlc_password)

    response = natural_language_classifier.classify(watson_nlc_id, text)
    top_class = response['top_class']
    print(getTopClassConfidence(top_class, response))
    if top_class == 'keskustelu':
        return None
    else:
        return top_class


def getUrl(url):
    """
    Desc:
        Returns the content of a given URL.
    Takes:
        str url : A URL of which's content is going to be returned.
    Returns:
        str content : The contents of the URL
    Note:
        None
    Raises:
        None
    """
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def downloadUrl(url, name):
    """
    Desc:
        Downloads the contents of the input URL.
    Takes:
        str url     : The URL to download
        str name    : The name for the downloaded content
    Returns:
        None
    Note:
        None
    Raises:
        None
    """
    wget.download(url, out=name)


def jsonFromUrl(url):
    """
    Desc:
        Returns a JSON object from the contents of a given URL.
    Takes:
        str url : The url where the JSON is
    Returns:
        dict js : The JSON from the URL as a dictionary
    Note:
        None
    Raises:
        None
    """
    content = getUrl(url)
    js = json.loads(str(content))
    return js


def getUpdates(offset=None):
    url = URL + 'getUpdates'
    if offset:
        url += '?offset={}'.format(offset)
    return jsonFromUrl(url)


def lastChatIdText(updates):
    """
    Desc:
        Gives the chat id of the last message sent.
    Takes:
        JSON updates : A JSON object of the same form as that is returned from the getUpdates() function.
    Returns:
        list conatining the last message text and the chat id of the last message sender.
    Note:
        Somewhat unstable fucntion at the moment.
    Raises:
        Exception('Ei ole viesti') when it cannot find any text from the last message sent.
    """
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    try:
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    except:
        try:
            text = updates["result"][last_update]["edited_message"]["text"]
            chat_id = updates["result"][last_update]["edited_message"]["chat"]["id"]
        except:
            try:
                text = updates["result"][last_update]["message"]["caption"]
                chat_id = updates["result"][last_update]["message"]["chat"]["id"]
            except:
                raise Exception('Ei ole viesti')
    return [text, chat_id]


def lastSenderId(update):
    """
    Desc:
        If the last message was sent via a group, the group id is returned instead.
    Takes:
        JSON update : A JSON object of the same form as that is returned from the getUpdates() function.
    Returns:
        str contaning the id of the sender or a group.
    Note:
        Possibly going to be removed a some point.
    Raises:
        None
     """
    if update['message']['chat']['type'] == 'group':
        return update['message']['chat']['id']
    if update['message']['chat']['type'] == 'private':
        return update['message']['from']['id']


def sendMessage(text, chat_id):
    """
    Desc:
        Sends a message with a given text to a given content.
    Takes:
        str text : The message that is going to be sent.
        str chat_id : the chat id that the message is being sent to.
    Returns:
        None
    Note:
        None
    Raises:
        None
    """
    text = urllib.parse.quote(text.encode('utf-8'))
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    print('Lähetin viestin: {} {}:lle'.format(text, chat_id))
    getUrl(url)


def getLastUpdateId(updates):
    """
    Desc:
        Returns the last update id.
    Takes:
        JSON updates : A JSON object of the same form as that is returned from the getUpdates() function.
    Returns:
        int update_id : The update id of the last update.
    Note:
        None
    Raises:
        None
    """

    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def getLastUpdate(updates):
    for i in updates['result']:
        if i['update_id'] == getLastUpdateId(updates):
            return i


def getFile(file_id, path):
    """
    Desc:
        Downloads an image from telegram servers.
    Takes:
        int file_id : Specifies which image is the one to be downloaded.
        str path : The local file path that the image is going to be saved to.
    Returns:
        None
    Note:
        None
    Raises:
        None
    """
    json = jsonFromUrl(URL + 'getFile?file_id={}'.format(file_id))
    url = 'https://api.telegram.org/file/bot{}/{}'.format(telegram_bot_token, json['result']['file_path'])
    downloadUrl(url, path)




def getMessageType(dictionary):
    """
    Desc:
        gets the type of the last message sent.
    Takes:
        dict dictionary : dictionary representing the last message.
    Returns:
        str : 'text' if the last message type is text, 'photo' if photo and 'caption' if an image with a caption
    Note:
        None
    Raises:
        None
    """
    if 'caption' in dictionary and 'photo' in dictionary:
        return 'caption'
    elif 'photo' in dictionary:
        return 'photo'
    elif 'text' in dictionary:
        return 'text'



def getChatTitle(update):
    """
    Desc:
        returns the chat title pf the last message sent.
    Takes:
        JSON update : A JSON object of the same form as that is returned from the getUpdates() function.
    Returns:
        str : chat title of the conversation that the last message was sent from.
    Note:
        None
    Raises:
        Exception('chatin titleä ei löytynyt') : If no chat title is not found.
    """
    if update['chat']['type'] == 'group':
        return update['chat']['title']
    elif update['chat']['type'] == 'private':
        return update['chat']['first_name']
    else:
        raise Exception('chatin titleä ei löytynyt')


def getMessageStuff(last_message):
    try:
        last_message_type = getMessageType(last_message['message'])
        last_message_content = last_message['message']
    except KeyError:
        try:
            last_message_type = getMessageType(last_message['edited_message'])
            last_message_content = last_message['edited_message']
        except:
            raise Exception('Not a message.')
    return (last_message_type, last_message_content)


def main():
    last_update_id = None
    while True:  # The super-duper-hyper-ultra-extra master champion aka main loop
        updates = getUpdates(last_update_id)
        if len(updates['result']) > 0:
            last_message = getLastUpdate(updates)  # The last "message" value in the getUpdates JSON object.
            last_message_type, last_message_content = getMessageStuff(last_message)
            last_update_id = getLastUpdateId(updates) + 1
            if last_message_type != 'photo':
                try:
                    chat_id = lastChatIdText(updates)[1]
                except Exception:
                    continue
            else:
                continue

    
        last_title = getChatTitle(last_message_content)
        chat_id = lastChatIdText(updates)[1]



if __name__ == '__main__':  # If a foreign script calls this file, it still works.
    main()
