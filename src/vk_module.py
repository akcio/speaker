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
        print(self.__userId)
        self.__speaker = speaker
        self.lastMessage = ''

    def getNewMessage(self):
        messages = self.api.messages.getDialogs(count=1)
        # print(messages)
        senderId = messages['items'][0]['message']['user_id'];
        if (senderId != self.__userId):
            sender = self.api.users.get(user_ids=senderId)
            message = messages['items'][0]['message']['body']
            toRead = sender[0]['last_name'] + ' ' + sender[0]['first_name'] + ' отправил вам сообщение. ' + message
            if (self.lastMessage != toRead):
                self.lastMessage = toRead
                self.__speaker.AddToQueue(toRead)
        Timer(5.0, self.getNewMessage).start()



# https://oauth.vk.com/authorize?client_id=4972828&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=2&response_type=token&v=5.80&state=123456

import requests
