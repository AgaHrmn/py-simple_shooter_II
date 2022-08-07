import pygame
from pygame.sprite import Sprite

class Meteor(Sprite):
    '''A class to represent single meteor in the group.'''
    def __init__(self, game):
        '''Initialize meteor and set it's position.'''
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen_rect

        self.image_path = r"python_crash_course\part_2\pygame_excercises\sideways_shooter\images\meteor.png"
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()

        self.rect.topright = self.screen_rect.topright 

        self.rect.right = self.screen_rect.right
        self.rect.y = 2* self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        '''Move meteor to the left.'''
        self.rect.x += self.settings.meteor_speed
        