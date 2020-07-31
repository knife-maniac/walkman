import board
from os import listdir
import RPi.GPIO as GPIO
import subprocess
import time


button1Pin = 25
button2Pin = 24
button3Pin = 23
button4Pin = 18


GPIO.setup(button1Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


mp3_files = [ f for f in listdir('songs') if f[-4:] == '.mp3' ]

if not len(mp3_files) > 0:
    print("No mp3 files found!")

print('\n--- Available mp3 files ---\n')
print('\n'.join(mp3_files))
print('\n---------------------------\n')

index = 0
a_song_is_currently_playing = False

while True:

    button1clicked = not GPIO.input(button1Pin)
    button2clicked = not GPIO.input(button2Pin)
    button3clicked = not GPIO.input(button3Pin)
    button4clicked = not GPIO.input(button4Pin)

        
    if button1clicked:
        index -= 1
        if index < 0:
            index = len(mp3_files)-1
        print("--- " + mp3_files[index] + " ---")

    if button2clicked:
        if a_song_is_currently_playing:
            subprocess.call(['killall', 'omxplayer.bin'])
        subprocess.Popen(['omxplayer', 'songs/' + mp3_files[index]])
        a_song_is_currently_playing = True
        time.sleep(0.25)
        
    if button3clicked:
        index += 1
        if index >= len(mp3_files):
            index = 0
        print("--- " + mp3_files[index] + " ---")
        
    if button4clicked and a_song_is_currently_playing:
        subprocess.call(['killall', 'omxplayer.bin'])
        print('--- Cleared all existing mp3s. ---')
        a_song_is_currently_playing = False

    time.sleep(0.25)