#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from SpeakerModule import Speaker
from whetherModule import Whether
from vk_module     import VKModule

import signal
import sys

def exit():
    print("Deleted all")
    del vk
    del w
    del s

    from threading import Timer
    Timer(5.0, sys.exit(0)).start()

if __name__ == "__main__":
    s = Speaker()
    w = Whether()
    vk = VKModule('', 0, s)
    # vk.getNewMessage()
    vk.getConversations()
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)
    # s.AddToQueue(w.GetStringForSpeach())
