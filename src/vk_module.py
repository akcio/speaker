import vk_requests
# from SpeakerModule import Speaker
import json

# s = Speaker()

previlegies = 40096+2
# print('https://oauth.vk.com/authorize?client_id=4972828&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope='+ str(previlegies) +'&response_type=token&v=5.80&state=123456')
#
# token = input("Paste token")
# s.AddToQueue("My letim na yamahe")
# s.AddToQueue("Тест")
# token = 'bace655acb6ca66c525a6f7cef61703cb98d92b8696ab78dee32805e58f9fae52d0bdaff0a8575be28bae'

# api = vk_requests.create_api(app_id=4972828 , service_token=token)
# # print(api.users.get(user_ids=1))
# messages = api.messages.getDialogs(count=50)
# # print(messages)
# senderId = messages['items'][0]['message']['user_id'];
# sender = api.users.get(user_ids=senderId)
# message = messages['items'][0]['message']['body']
# toRead = sender[0]['last_name'] + ' ' + sender[0]['first_name'] + ' отправил вам сообщение. ' + message
# s.AddToQueue(toRead)

from threading import Timer

class VKModule():

    def __init__(self, token, userId, speaker):
        self.api = vk_requests.create_api(app_id=4972828 , service_token=token)
        self.__userId = userId
        self.__userCache = []
        self.__readedMsgs = []
        self.__timer = None
        print(self.__userId)
        self.__speaker = speaker
        self.lastMessage = ''
        self.loadCach()

    def loadCach(self):
        from os import path
        import json
        if path.isfile('cache.cached'):
            with open('cache.cached', 'r') as the_file:
                text = the_file.read()
                try:
                    text = json.loads(text)
                except:
                    text = []
                if 'users' in text:
                    self.__userCache = text['users']
                    print('Cached users loaded')
                    print(self.__userCache)
                if 'readedMesages' in text:
                    self.__readedMsgs = text['readedMesages']
                    if self.__readedMsgs.__len__() > 5:
                        self.__readedMsgs = self.__readedMsgs[10:]
                    print('Readed messages loaded')
                    print(self.__readedMsgs)


    def __delete__(self, instance):
        instance.__del__()

    def __del__(self):
        print('tmp')
        self.__timer.cancel()
        import json
        with open('cache.cached', 'w') as the_file:
            the_file.write(json.dumps({'users': self.__userCache, 'readedMesages': self.__readedMsgs}))

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('tmp')
        self.__timer.cancel()
        import json
        with open('cache.cached', 'w') as the_file:
            the_file.write(json.dumps({'users' : self.__userCache, 'readedMesages' : self.__readedMsgs}))

    def getNewMessage(self):
        messages = self.api.messages.getDialogs(count=1)
        # print(messages)
        senderId = messages['items'][0]['message']['user_id'];
        if (senderId != self.__userId and messages['items'][0]['message']['out'] != 1):
            sender = self.api.users.get(user_ids=senderId)
            message = messages['items'][0]['message']['body']
            print(messages['items'][0]['message'])
            toRead = sender[0]['last_name'] + ' ' + sender[0]['first_name'] + ' отправил вам сообщение. ' + message
            if (self.lastMessage != toRead):
                self.lastMessage = toRead
                self.__speaker.AddToQueue(toRead)
        self.__timer = Timer(5.0, self.getNewMessage).start()

    def getCounters(self):
        response = self.api.account.getCounters()
        messages = 0
        friends = 0
        gifts = 0
        if ('messages' in response):
            messages = int(response['messages'])
        if 'friends' in response:
            friends = int(response['friends'])
        if 'gifts' in response:
            gifts = int(response['gifts'])
        return {'messages' : messages, 'friends' : friends, 'gifts' : gifts}

    def __findUserInCache(self, userId):
        for item in self.__userCache:
            if item['userId'] == userId:
                return item
        return None


    def getUserInfo(self, userId):
        founded = self.__findUserInCache(userId)
        if (founded == None):
            users = self.api.users.get(user_ids=userId, fields='bdate')
            user = {'userId' : userId, 'last_name' : '', 'first_name' : '', 'bdate' : ''}
            if 'id' in users[0]:
                user['userId'] = users[0]['id']
            if 'last_name' in users[0]:
                user['last_name'] = users[0]['last_name']
            if 'first_name' in users[0]:
                user['first_name'] = users[0]['first_name']
            if 'bdate' in users[0]:
                user['bdate'] = users[0]['bdate']
            self.__userCache.append(user)
            founded = user
        return founded

    def getConversations(self):
        response = self.api.messages.getConversations(filter='unread', extended=1)

        if 'items' in response:
            for obj in response['items']:
                lastMessage = obj['last_message']
                if (lastMessage['id'] in self.__readedMsgs):
                    continue
                user = self.getUserInfo(lastMessage['from_id'])
                text = lastMessage['text']
                self.__readedMsgs.append(lastMessage['id'])
                if 'attachments' in lastMessage:
                    for attachment in lastMessage['attachments']:
                        if attachment['type'] == 'photo':
                            text += ' фотография,'
                        if attachment['type'] == 'video':
                            text += ' видео ' + attachment['video']['title'] + ','
                        if attachment['type'] == 'audio':
                            text += ' трек ' + attachment['audio']['title'] + ','
                        if attachment['type'] == 'doc':
                            text += ' документ ' + attachment['doc']['title'] + ','

                        if attachment['type'] == 'link':
                            text += ' ссылку ' + attachment['link']['title'] + ','
                        if attachment['type'] == 'wall':
                            text += ' запись на стене ' + attachment['wall']['text'] + ','
                        if attachment['type'] == 'wall_reply':
                            text += ' комментарий на стене ' + attachment['wall']['text'] + ','
                        if attachment['type'] == 'sticker':
                            text += ' стикер,'
                        if attachment['type'] == 'gift':
                            text += ' подарок,'

                toRead = user['last_name'] + ' ' + user['first_name'] + ' отправил вам сообщение. ' + text
                self.__speaker.AddToQueue(toRead)
        # print(response)
        self.__timer = Timer(5.0, self.getConversations).start()

# https://oauth.vk.com/authorize?client_id=4972828&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=2&response_type=token&v=5.80&state=123456

import requests
