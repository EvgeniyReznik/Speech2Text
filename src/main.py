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
import subprocess
import pyttsx
from ctypes import *

def Talk(text):
    
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)
    engine.say('Hi, what do you want my dear friend?')
    engine.runAndWait()
    
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
    cmdline = 'C:\TotalAudioConverter\AudioConverter.exe C:\Users\Evgeniy\workspace\Speech2TextEngine\src\output.wav C:\Users\Evgeniy\workspace\Speech2TextEngine\src\output.flac'
    os.system(cmdline)
    print "Done"

def Send():
    global ANSWER
    url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-EN'
    url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US&maxresults=10&pfilter=0"
    flac=open('C:\Users\Evgeniy\workspace\Speech2TextEngine\src\output.flac',"rb").read()
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
    os.remove('C:\Users\Evgeniy\workspace\Speech2TextEngine\src\output.wav')
    os.remove('C:\Users\Evgeniy\workspace\Speech2TextEngine\src\output.flac')
    return ANSWER

def Processing():
    global ANSWER
    if ANSWER == 0:
        return 0
    elif 'chrome' in ANSWER.lower():
        os.system('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')

    elif 'skype' in ANSWER.lower():
        os.system('C:\Program Files (x86)\Skype\Phone\Skype.exe')
    
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
        
    print ('Hi, what do you want?')
    Talk('Hi, what do you want my dear friend?')
    Record()
    Convert()
    print ('Sending...')
    Send()
    print 'Done'
    Processing()
    
    while True:
        ANSWER = None
        #Talk('Done.')
        print 'Do you want something else? (Your command\No)'
        Talk('Do you want something else??')
        Record()
        Convert()
        print 'Sending...'
        Send()
        print 'Done'
    
        #print ANSWER
        if ANSWER == 0:
            continue
     
        if ANSWER.lower()== 'no' or\
            ANSWER.lower()== 'nope' or\
            ANSWER.lower()== 'not' or\
            ANSWER.lower()== 'nay':
            break
        else:
            Processing()
    
    print 'Okay, bye'
    Talk('Okay, bye')
    pass