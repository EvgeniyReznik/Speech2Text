'''
Created on Jul 25, 2015

@author: Evgeniy
'''


import time, pyaudio 
import wave, os, urllib
import urllib2, pycurl
import httplib, sys, string
import win32api 
import win32con 
from ctypes import *

def Talk(text):
 
 def downloadFile(url, fileName):
    fp = open(fileName, "wb")
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, fp)
    curl.perform()
    curl.close()
    fp.close()

 def getGoogleSpeechURL(phrase):
    googleTranslateURL = "http://translate.google.com/translate_tts?tl=en&"
    parameters = {'q': phrase}
    data = urllib.urlencode(parameters)
    googleTranslateURL = "%s%s" % (googleTranslateURL,data)
    return googleTranslateURL

 def speakSpeechFromText(phrase):
    googleSpeechURL = getGoogleSpeechURL(phrase)
    downloadFile(googleSpeechURL,"ans.mp3")
 
 speakSpeechFromText(text)
 pass


if __name__ == '__main__':
    print("hi i am alive")

    winmm = windll.winmm
    winmm.mciSendStringA('Open "ans.mp3" Type MPEGVideo Alias theMP3',0,0,0)
    winmm.mciSendStringA('Play theMP3 Wait',0,0,0)
    winmm.mciSendStringA("Close theMP3","",0,0)
    print("Thats it folks!@")
    pass