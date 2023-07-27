import pygame

pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Label():
    def __init__(self, screen, txt, location, size=(150, 50), bgc=BLACK, fgc=WHITE, font_name="comicsans", font_size=28):
        self.txt = txt
        self.size = size
        self.bgc = bgc
        self.fgc = fgc
        self.screen = screen
        self.x, self.y = location
        
        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        
        self.font = pygame.font.Font(font_name, font_size)
        self.txt_surf = self.font.render(self.txt, 1, fgc)
        self.txt_rect = self.txt_surf.get_rect(topleft=self.rect.topleft)

    def draw(self):
        self.surface.fill(self.bgc)
        self.surface.blit(self.surface, self.rect)
        self.screen.blit(self.txt_surf, self.txt_rect)
        pygame.display.update()

    def update(self):
        self.txt_surf = self.font.render(self.txt, 1, self.fgc)
        self.surface = pygame.surface.Surface(self.size)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        self.txt_rect = self.txt_surf.get_rect(topleft=self.rect.topleft)
        self.draw()

    def set_default_size(self):
        self.size = (self.txt_surf.get_width() + 10, self.txt_surf.get_height() + 10)

    def get_width(self):
        return self.size[0]
    
    def get_height(self):
        return self.size[1]

