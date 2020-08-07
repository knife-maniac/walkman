import board
import os
import pygame
import RPi.GPIO as GPIO
import time

class Button:
    def __init__(self, pin, state):
        self.pin = pin
        self.state = state
    
previous_button = Button(25, False)
play_button = Button(24, False)
next_button = Button(23, False)
stop_button = Button(18, False)

buttons = [previous_button, play_button, next_button, stop_button]

for button in buttons:
    GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mp3_files = os.listdir('songs')

if not len(mp3_files):
    print("No mp3 files found!")

print('\n--- Available mp3 files ---\n')
print('\n'.join(mp3_files))
print('\n---------------------------\n')


index = 0
a_song_is_currently_playing = False
song_is_paused = False

pygame.init()
music = pygame.mixer.music

def change_song_and_get_new_index(direction, songs, index):
    if direction=='previous':
        index -= 1
        if index < 0:
            index = len(songs)-1
    elif direction=='next':
        index += 1
        if index >= len(songs):
            index = 0
    elif direction=='random':
        if len(songs)!=1:
            new_index = -1
            while new_index != index:
               new_index = random.randint(0, len(songs)-1)
            index = new_index
    
    print("--- " + mp3_files[index] + " ---")        
    music.load('songs/' + mp3_files[index])
    return index


walkman_is_on = True

while walkman_is_on:
    a_song_is_currently_playing = music.get_busy()
    
    for button in buttons:
        button.state = not GPIO.input(button.pin)    


    if previous_button.state:
        index = change_song_and_get_new_index('previous', mp3_files, index)

    if play_button.state:
        if not a_song_is_currently_playing:
            music.load('songs/' + mp3_files[index])
            music.play()
        elif song_is_paused:
            music.unpause()
            song_is_paused = False
        
    elif not song_is_paused:
        music.pause()
        song_is_paused = True


    if next_button.state:
        index = change_song_and_get_new_index('next', mp3_files,index)
        
    if stop_button.state:
        music.stop()
        walkman_is_on = False
        

    time.sleep(0.25)

os.system('sudo shutdown -h now')