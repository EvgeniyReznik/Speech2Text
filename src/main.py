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
import speech_recognition as sr
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
    r = sr.Recognizer()
    with sr.WavFile("output.wav") as source:              # use "output.wav" as the audio source
        audio = r.record(source)                        # extract audio data from the file
    try:
        list = r.recognize(audio,True)                  # generate a list of possible transcriptions
        print("Possible transcriptions:")
        for prediction in list:
            print(" " + prediction["text"] + " (" + str(prediction["confidence"]*100) + "%)")
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")
    
    return list

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
#     Convert()
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