import pygame
import time

file_path = "output.mp3"


def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # Wait for the sound to finish playing
        time.sleep(0.1)

def music_function():
    play_mp3(file_path)

# music_function()
