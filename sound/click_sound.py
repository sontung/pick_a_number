import pygame


pygame.mixer.init()
sound_object = pygame.mixer.Sound("sound/beep1.ogg")
sound_object.set_volume(1)
