import pygame,sys,os
#carrega a pasta do jogo
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,'img')
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

FPS = 27
WIDTH = 800
HEIGHT = 600
def load_img(name, width = 50,height=50):
    return pygame.transform.scale(pygame.image.load(os.path.join(img_folder, name)).convert(), (width,height))
class Ship(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y, speed=[30,30]):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_img('player.png',100)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.width = self.rect.width
        self.radius =  self.rect.width*.75/2#75%
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x, self.rect.y = pos_x, pos_y-self.height
        self.speed = speed
        self.lifes = 3
    def update(self):
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.x+self.speed[0]+self.width < WIDTH:
            self.rect.x += self.speed[0]
        if pygame.key.get_pressed()[pygame.K_a] and self.rect.x -self.speed[0]+self.width > self.width:
            self.rect.x -= self.speed[0]
        if pygame.key.get_pressed()[pygame.K_w] and self.rect.y-self.speed[1]+self.height > self.height:
            self.rect.y -= self.speed[1]
        if pygame.key.get_pressed()[pygame.K_s] and self.rect.y +self.speed[1]+self.height < HEIGHT:
            self.rect.y += self.speed[1]
    def damage(self):
        self.lifes -= 1
        print(f"dano-> suas vidas{self.lifes}")
        self.rect.x, self.rect.y = WIDTH/2, HEIGHT-self.height
class Enemy(pygame.sprite.Sprite):
    def __init__(self,width,height, color, pos_x, pos_y, speed=[10,5]):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_img('alien.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.radius = 25
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption("Space Game")
        pygame.display.set_icon(pygame.image.load(os.path.join(img_folder, "planet01b.png")))
        self.clock = pygame.time.Clock()
    #grupos de sprites 
        self.all_sprites = pygame.sprite.Group()
    #instancia do jogo
        self.ship = Ship(WIDTH/2, HEIGHT)
        self.enemy = Enemy(50,50,RED, (WIDTH/2)-50, 0)
        self.all_sprites.add(self.ship)
        self.all_sprites.add(self.enemy)

        self.background = load_img("bg2.png", WIDTH, HEIGHT)
    def run(self):
        while 1:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    global WIDTH,HEIGHT
                    self.screen = pygame.display.set_mode(event.size,pygame.RESIZABLE)
                    WIDTH, HEIGHT = event.size
                    self.background = load_img("bg2.png", WIDTH, HEIGHT)
                    
            #atualiza os sprites

            self.all_sprites.update()
            self.collision()
            self.screen.blit(self.background,[0,0])

            self.all_sprites.draw(self.screen)
            pygame.display.update() #flip
    def collision(self):
        #colisão corpo a corpo inimigo-heroi
            if pygame.sprite.groupcollide(pygame.sprite.GroupSingle(self.ship), pygame.sprite.GroupSingle(self.enemy), False, False):
                self.ship.damage()
if __name__ ==  '__main__':
    game = Game()
    game.run()
