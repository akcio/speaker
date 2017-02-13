#!/usr/bin/env python2
#encoding: UTF-8
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
class Speaker():
    
    def __init__(self):
        self.messagePool = []
        self.TimerSpeach()
    
    def TimerSpeach(self):
        import threading
        threading.Timer(5.0, self.TimerSpeach).start()
        if (self.messagePool != []):
            self.messagePool.reverse()
            self.SpeakTest(self.messagePool.pop())
            self.messagePool.reverse()

    def AddToQueue(self, text):
        self.messagePool.append(text)
    
    def SpeakTest(self, text):
        import subprocess
        speach = '"' + text + '" '
        print speach
        #text = '«Hello world» "
        subprocess.call ('espeak -vru -s 60 ' + speach, shell = True)
        
#s = Speaker()
#s.AddToQueue('123')
#s.AddToQueue('Василий')
#s.AddToQueue('Молодец')

