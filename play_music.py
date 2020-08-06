import board
from os import listdir
import pygame
import RPi.GPIO as GPIO
import time


PINS = [25, 24, 23]
for pin in PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mp3_files = [ f for f in listdir('songs') if f[-4:] == '.mp3' ]

if not len(mp3_files) > 0:
    print("No mp3 files found!")

print('\n--- Available mp3 files ---\n')
print('\n'.join(mp3_files))
print('\n---------------------------\n')


index = 0
a_song_is_currently_playing = False
song_is_paused = False

pygame.init()
buttons_state = [False, False, False]

while True:
    a_song_is_currently_playing = pygame.mixer.music.get_busy()
    buttons_state = list(not GPIO.input(PINS[button]) for button in range(3))
    
        
    if buttons_state[0]:
        index -= 1
        if index < 0:
            index = len(mp3_files)-1
        print("--- " + mp3_files[index] + " ---")
        pygame.mixer.music.load('songs/' + mp3_files[index])

    if buttons_state[1]:
        if song_is_paused:
            pygame.mixer.music.unpause()
            song_is_paused = False
        if not a_song_is_currently_playing:
            pygame.mixer.music.load('songs/' + mp3_files[index])
            pygame.mixer.music.play()
    elif not song_is_paused:
        pygame.mixer.music.pause()
        song_is_paused = True
        
    if buttons_state[2]:
        index += 1
        if index >= len(mp3_files):
            index = 0
        print("--- " + mp3_files[index] + " ---")
        pygame.mixer.music.load('songs/' + mp3_files[index])

        
    time.sleep(0.25)