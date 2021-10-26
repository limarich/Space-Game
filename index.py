import pygame,sys,os,random
"""carrega a pasta do jogo"""
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,'img')

"""Variáveis úteis"""
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

FPS = 27
WIDTH = 800
HEIGHT = 600
def load_img(name, width = 50,height=50):
    """
    Função que carrega as imagens presentes dentro da pasta do jogo 
    """
    return pygame.transform.scale(pygame.image.load(os.path.join(img_folder, name)).convert(), (width,height))
class Ship(pygame.sprite.Sprite):
    """
    Nave do jogador
    """
    def __init__(self, speed=[30,30]):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_img('player.png',100)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.width = self.rect.width
        self.radius =  self.rect.width*.75/2#75%
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x, self.rect.y = WIDTH/2, HEIGHT-self.height
        self.speed = speed
        self.lifes = 3
    def update(self):
        """
        Atualização do jogador
        """
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.x+self.speed[0]+self.width < WIDTH:
            self.rect.x += self.speed[0]
        if pygame.key.get_pressed()[pygame.K_a] and self.rect.x -self.speed[0]+self.width > self.width:
            self.rect.x -= self.speed[0]
        if pygame.key.get_pressed()[pygame.K_w] and self.rect.y-self.speed[1]+self.height > self.height:
            self.rect.y -= self.speed[1]
        if pygame.key.get_pressed()[pygame.K_s] and self.rect.y +self.speed[1]+self.height < HEIGHT:
            self.rect.y += self.speed[1]
    def shoot(self):
        """
        Instancia de tiros do jogador
        """
        return Bullet(self.rect.centerx,self.rect.top)
    def damage(self):
        """
        Ativa as ações de dano do jogador
        """
        self.lifes -= 1
        print(f"dano-> suas vidas{self.lifes}")
        self.rect.x, self.rect.y = WIDTH/2, HEIGHT-self.height
class Enemy(pygame.sprite.Sprite):
    """Nave Inimiga padrão"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_img('alien.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x, self.rect.y = random.randrange(0, WIDTH - self.rect.width),  random.randrange(-200,-40)
        self.speedx = random.randrange(-3,3)
        self.speedy = random.randrange(1,8)
    def update(self):
        """Atualização da nave inimiga""" 
        self.rect.x +=self.speedx
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT + 10 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
class Bullet(pygame.sprite.Sprite):
    """
    Classe do tiro das naves 
    """
    def __init__(self,x,y):
         pygame.sprite.Sprite.__init__(self)
         self.image = load_img("planet02.png",10,30)
         self.image.set_colorkey(WHITE)
         self.rect = self.image.get_rect()
         self.speedy = -10
         self.rect.bottom = y
         self.rect.centerx = x
    def update(self):
        "Atualização dos tiros"
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class Game():
    def __init__(self, n_enemies=10):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption("Space Game")
        pygame.display.set_icon(pygame.image.load(os.path.join(img_folder, "planet01b.png")))
        self.clock = pygame.time.Clock()
    #grupos de sprites 
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.ship = Ship()
        self.all_sprites.add(self.ship)
        for i in range(n_enemies):
            e = Enemy()
            self.all_sprites.add(e)
            self.enemies.add(e)

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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        shoot = self.ship.shoot()
                        self.all_sprites.add(shoot)
                        self.bullets.add(shoot)
            #atualiza os sprites

            self.all_sprites.update()
            self.collision()
            self.screen.blit(self.background,[0,0])

            self.all_sprites.draw(self.screen)
            pygame.display.update() #flip
    def collision(self):
        #colisão corpo a corpo inimigo-heroi
        # for enemy in self.enemies:
        if pygame.sprite.spritecollide(self.ship, self.enemies, False,False):
            self.ship.damage()
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets,True, True)
        for hit in hits:
            e = Enemy()
            self.all_sprites.add(e)
            self.enemies.add(e)
if __name__ ==  '__main__':
    game = Game()
    game.run()
