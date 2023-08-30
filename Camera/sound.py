import pygame
import time


def play_sound(sound_file):
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    while pygame.mixer.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()


if __name__ == "__main__":
    sound_file = r'Camera\beep-07a.wav'
    play_sound(sound_file)
