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

def Record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Done recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def Convert():
    print "Converting"
    os.system('C:\Users\Егор\Desktop\Расширение\TotalAudioConverter\AudioConverter.exe C:\Users\Егор\Desktop\Расширение\output.wav C:\Users\Егор\Desktop\Расширение\output.flac')
    print "Done"

def Send():
    global ANSWER
    url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-EN'
    flac=open('output.flac',"rb").read()
    header = {'Content-Type' : 'audio/x-flac; rate=16000'}
    req = urllib2.Request(url, flac, header)
    data = urllib2.urlopen(req)
    a = data.read()
    ANSWER = eval(a)
    if ANSWER['status'] == 5:
        print 'Sorry, I do not understand you.'
        Talk('Sorry, I do not understand you.')
        ANSWER = 0

    else:
        ANSWER = ANSWER['hypotheses'][0]['utterance']
        print ANSWER
    os.remove('C:\Users\Егор\Desktop\Расширение\output.wav')
    os.remove('C:\Users\Егор\Desktop\Расширение\output.flac')
    return ANSWER

def Processing():
    global ANSWER
    if ANSWER == 0:
        return 0
    elif 'chrome' in ANSWER.lower():
        os.system('C:\Users\Егор\AppData\Local\Google\Chrome\Application\chrome.exe')

    elif 'skype' in ANSWER.lower():
        os.system('C:\Users\Егор\Downloads\SkypePortable\SkypePortable.exe')
    
    elif 'cd rom' in ANSWER.lower() or\
        'cd-rom' in ANSWER.lower() or\
        'open d' in ANSWER.lower() or\
        'dvd' in ANSWER.lower() or\
        'dvd-rom' in ANSWER.lower() or\
        'dvd rom' in ANSWER.lower() or\
        'cdrom' in ANSWER.lower() or\
        'cd - rom' in ANSWER.lower():
        winmm = windll.winmm
        winmm.mciSendStringA("set cdaudio door open", "", 0,0)

if __name__ == '__main__':
    print("hi i am alive")

    winmm = windll.winmm
    winmm.mciSendStringA('Open "ans.mp3" Type MPEGVideo Alias theMP3',0,0,0)
    winmm.mciSendStringA('Play theMP3 Wait',0,0,0)
    winmm.mciSendStringA("Close theMP3","",0,0)
    print("Thats it folks!@")
    pass