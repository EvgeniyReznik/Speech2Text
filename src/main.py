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
from win32con import NULL

def Talk(text):
    
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)
    engine.say(text)
    engine.runAndWait()
    
    pass

def Record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
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
    def callback(recognizer, audio):                          # this is called from the background thread
        try:
            print("You said " + recognizer.recognize(audio))  # received audio data, now need to recognize it
        except LookupError:
            print("Oops! Didn't catch that")
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source: r.adjust_for_ambient_noise(source)      # we only need to calibrate once, before we start listening
    stop_listening = r.listen_in_background(m, callback)
    
    for _ in range(50): time.sleep(0.1)                       # we're still listening even though the main thread is blocked - loop runs for about 5 seconds
    stop_listening()                                          # call the stop function to stop the background thread
    while True: time.sleep(0.1)                               # the background thread stops soon after we call the stop function

def Processing():
    ANSWER = 0
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
    Talk('Hi, what do you want?')
    
    Record()
#     Convert()
    print ('Sending...')
    Send()
    print 'Done'
    Processing()
    
    print 'Okay, bye'
    Talk('Okay, bye')
    pass