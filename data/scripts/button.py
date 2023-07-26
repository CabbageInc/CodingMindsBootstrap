import random
import time
import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self): # Add given properties as parameters
        pygame.sprite.Sprite.__init__(self)
        # Initialize properties here

        self.image = pygame.Surface((230, 230))
        self.image.fill(self.color_off)
        self.rect = self.image.get_rect()
        # Assign x, y coordinates to the top left of the sprite
        self.rect.topleft = ()
        self.clicked = False
        '''
        Draws button sprite onto pygame window when called
        '''

    def draw(self, screen):
        # blit image here
        '''
        Used to check if given button is clicked/selected by player
        '''
        
    def selected(self, mouse_pos):
        # Check if button was selected. Pass in mouse_pos.
        '''
        Illuminates button selected and plays corresponding sound.
        Sets button color back to default color after being illuminated.
        '''

    def update(self, screen):
        # Illuminate button by filling color here
        # blit the image here so it is visible to the player
        # Play sound
        pygame.display.update()
        self.image.fill(self.color_off)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.time.wait(500)
        pygame.display.update()