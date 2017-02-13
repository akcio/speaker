#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from SpeakerModule import Speaker
from whetherModule import Whether

if __name__ == "__main__":
    s = Speaker()
    w = Whether()
    s.AddToQueue(w.GetStringForSpeach())
