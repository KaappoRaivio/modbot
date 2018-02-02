import json
import requests
import time
import wget
from watson_developer_cloud import NaturalLanguageClassifierV1
import telegram
import os
import urllib

os.chdir(os.environ['HOME']  + '/laksybot/ryhmät')



TOKEN = '525786228:AAHE36X67LKReTNYYwQ4wZQ6VhlVK94Hwk8' # "386957960:AAEWqf1iFMjnHk7yJfqK9pHVuWiTaxQpJ1I" #This is for the authentication of the bot.
lxybot = telegram.Bot(TOKEN)
URL = "https://api.telegram.org/bot{}/".format(TOKEN)



def getUrl(url): # Opens a url
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def downloadUrl(url, name): #Downloads the contents of the input url.
    wget.download(url,out=name)


def jsonFromUrl(url): #Returns a json object from the contents of a given url.
    content = getUrl(url)
    js = json.loads(content)
    return js

def getUpdates(): # Returns a JSON object representing the events that occur during interacting with the bot.
    url = URL + "getUpdates?timeout=100&alllowed_updates=['message']"
    js = jsonFromUrl(url)
    return js


def getUpdatesWithOffset(offset=None):
    url = URL + "getUpdates?timeout=100&alllowed_updates=['message']&offset={}".format(offset)
    js = jsonFromUrl(url)
    return js

def getLastUpdateId(updates): #Gets the highest id, and thus last, id from the JSON object that is returned by the getUpdates function.
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def getLastUpdate(updates): # Returns the last event that is visible in the getUpdates JSON object.
    update_ids = []
    if len(updates['result']) == 0:
        raise Exception('No messages yet')
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    for i in updates['result']:
        if i['update_id'] == max(update_ids):
            return i


def getFile(file_id, path): #Downloads an image from telegram servers specified by an image id. path is the location that the image is going to be saved to.
    json = jsonFromUrl(URL + 'getFile?file_id={}'.format(file_id))
    url = 'https://api.telegram.org/file/bot{}/{}'.format( TOKEN, json['result']['file_path'])
    downloadUrl(url, path)


def getFileId(resolution): # Gets the id of the best-quality image.
    updates = getUpdates()
    greatest = 0
    for j,i in enumerate(updates['result']):
        if i['update_id'] == getLastUpdateId(updates):
            path = updates['result'][j]['message']['photo']
            break
    if resolution:
        for i in path:
            if i['file_size'] > greatest:
                greatest = i['file_size']
        for i in path:
            if i['file_size'] == greatest:
                return i['file_id']
    else:
        for i in path:
            if i['file_size'] < greatest:
                greatest = i['file_size']
        for i in path:
            if i['file_size'] == greatest:
                 return i['file_id']


def getMessageType(dictionary): # Returns the type of the last message sent.
    if 'caption' in dictionary:
        return 'caption'
    elif 'photo' in dictionary:
        return 'photo'
    elif 'text' in dictionary:
        return 'text'



def main():
    counter = 0
    print(getUpdates()['result'])
    for i in getUpdates()['result']:
        print('\n' + str(counter))
        getFile(i['message']['photo'][len(i['message']['photo']) - 1]['file_id'], '/home/kaappo/Desktop/epäspammikuvat/asd{}.jpg'.format(counter))
        counter += 1


if __name__ == '__main__': # If a foreign script calls this file, it still works.
    main()
