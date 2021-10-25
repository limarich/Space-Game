import pygame,sys
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

WIDTH = 800
HEIGHT = 600
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
class Ship(pygame.sprite.Sprite):
    def __init__(self,width,height, color, pos_x, pos_y, speed=[10,5]):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y
        self.speed = speed
    def update(self):
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.x+self.speed[0]+self.width < WIDTH:
            self.rect.x += self.speed[0]
        if pygame.key.get_pressed()[pygame.K_a] and self.rect.x -self.speed[0]+self.width > self.width:
            self.rect.x -= self.speed[0]
        if pygame.key.get_pressed()[pygame.K_w] and self.rect.y-self.speed[1]+self.height > self.height:
            self.rect.y -= self.speed[1]
        if pygame.key.get_pressed()[pygame.K_s] and self.rect.y +self.speed[1]+self.width < HEIGHT:
            self.rect.y += self.speed[1]
class Enemy(pygame.sprite.Sprite):
    def __init__(self,width,height, color, pos_x, pos_y, speed=[10,5]):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y
        self.speed = speed
    def update(self):
        self.rect.x += self.speed[0]
        if self.rect.x > WIDTH:
            self.rect.x = WIDTH-self.width
            self.speed[0]*=-1
        if self.rect.x < 0:
            self.speed[0]*=-1
            self.rect.x = self.width


def main():
    clock = pygame.time.Clock()
    #grupos de sprites 
    all_sprites = pygame.sprite.Group()
    #instancia do jogo
    game = Game()
    ship = Ship(10,10, WHITE, WIDTH/2, HEIGHT-10)
    enemy = Enemy(50,50,RED, (WIDTH/2)-50, 0)
    all_sprites.add(ship)
    all_sprites.add(enemy)

    while 1:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        #atualiza os sprites
        all_sprites.update()

        game.screen.fill(BLACK)
        all_sprites.draw(game.screen)
        pygame.display.update() #flip
main()
