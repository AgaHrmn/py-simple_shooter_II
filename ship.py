import pygame
from settings import Settings
from pygame.sprite import Sprite

class Ship(Sprite):
    '''Class to manage player.'''
    def __init__(self, game):
        super().__init__()
        self.player_path = r"python_crash_course\part_2\pygame_excercises\sideways_shooter\images\player.png"
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        self.image = pygame.image.load(self.player_path)
        self.rect = self.image.get_rect()

        self.rect.midleft = self.screen_rect.midleft

    ship_up = False
    ship_down = False

    def update(self):
        if self.ship_up and self.rect.top > 50:
            self.rect.y -= self.settings.ship_speed
        elif self.ship_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.ship_speed + 1

    def center_ship(self):
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
        
    def blit_player(self):
        self.screen.blit(self.image, self.rect)
