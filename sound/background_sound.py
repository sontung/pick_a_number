import pygame
pygame.mixer.init()


def play_music(name, type):
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load(name)
    if type == "click":
        pygame.mixer.music.play(1, 0.0)
    else:
        pygame.mixer.music.play(-1, 0.0)


def stop_music():
    pygame.mixer.music.stop()

music_funcs = (play_music, stop_music)
