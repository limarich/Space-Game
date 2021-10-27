# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import pygame,sys,os,random
from pygame.constants import USEREVENT
pygame.init()

"""carrega a pasta do jogo + arquivos"""
game_folder = os.path.dirname(__file__)
game_font = os.path.join(game_folder,'fonts') + '\stocky.ttf'
img_folder = os.path.join(game_folder,'img')
snd_dir = os.path.join(game_folder,'sounds')
"""Variáveis úteis"""
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

FPS = 27
WIDTH = 800
HEIGHT = 600
#sons
def load_sound(name):
    """carrega os audios da pasta do jogo"""
    return pygame.mixer.Sound(os.path.join(snd_dir, name))
shoot_sound =  load_sound("Laser_Shoot2.wav")
Bomb_sound =  load_sound("Bomb.wav")
expl_sound = [load_sound("Explosion1.wav"), load_sound("Explosion2.wav")]
hurt_sound = load_sound("Hit_Hurt.wav")


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
        self.image = load_img('player2.png',50,30)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.width = self.rect.width
        self.radius =  self.rect.width*.75/2#75%
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x, self.rect.y = WIDTH/2, HEIGHT-self.height
        self.speed = speed
        self.lifes = 3
        self.missiles = 3
        self.last_update = pygame.time.get_ticks()
    def update(self):
        """
        Atualização do jogador
        """
        self.last_update = pygame.time.get_ticks()
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
        shoot_sound.play()
        return Bullet(self.rect.centerx,self.rect.top)
    def damage(self, game):
        """
        Ativa as ações de dano do jogador
        """
        self.lifes -= 1
        if self.lifes <= 0:
            self.kill()
            game.end =  1
        self.rect.x, self.rect.y = WIDTH/2, HEIGHT-self.height
    def bomb(self):
        """
        cria animação da bomba e desconta o total de bombas do player
        """
        Bomb_sound.play()
        return Bomb(self.rect.centerx,self.rect.top)
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
         self.image = load_img("bullet.png",10,30)
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
class Bomb(pygame.sprite.Sprite):
    """
    Classe da bomba do player
    """
    def __init__(self,x,y):
         pygame.sprite.Sprite.__init__(self)
         self.image = pygame.transform.rotate(load_img("missile_half.png"),90)
         self.image.set_colorkey(WHITE)
         self.rect = self.image.get_rect()
         self.speedy = -15
         self.rect.bottom = y
         self.rect.centerx = x
    def update(self):
        "Atualização da bomba"
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class Game():
    pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.mp3'))
    pygame.mixer.music.play(loops=-1)
    def __init__(self, n_enemies=10):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption("Space Game")
        pygame.display.set_icon(pygame.image.load(os.path.join(img_folder, "planet01b.png")))
        self.clock = pygame.time.Clock()
        #grupos de sprites 
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.n_enemies = n_enemies
        self.ship = Ship()
        self.all_sprites.add(self.ship)
        self.score = 0
        self.end = 0
        for i in range(n_enemies):
            e = Enemy()
            self.all_sprites.add(e)
            self.enemies.add(e)
        self.background = load_img("bg.png", WIDTH, HEIGHT)
    def run(self):
        shot_speed = 0
        while not self.end:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    global WIDTH,HEIGHT
                    self.screen = pygame.display.set_mode(event.size,pygame.RESIZABLE)
                    WIDTH, HEIGHT = event.size
                    self.background = load_img("bg.png", WIDTH, HEIGHT)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.ship.missiles > 0:
                        self.ship.missiles -=1
                        self.all_sprites.add(self.ship.bomb())
                        for enemy in self.enemies:
                            self.score += 50
                            enemy.kill()
                        for i in range(self.n_enemies): #respanw
                            self.respawn_enemy()
            
            #atualiza os sprites
            if shot_speed % 10 == 0:
                shoot = self.ship.shoot()
                self.all_sprites.add(shoot)
                self.bullets.add(shoot)


            self.all_sprites.update()
            self.collision()
            self.screen.blit(self.background,[0,0])
            self.all_sprites.draw(self.screen)
            self.draw_text(f"score:{self.score}", 20, WIDTH/2, 10)
            self.draw_text(f"Vidas:{self.ship.lifes}", 20, 50, 10)
            self.draw_text(f"Misseis:{self.ship.missiles}", 20, 60, 40)
            shot_speed+=1
            pygame.display.update() #flip
            self.game_over()
    def game_over(self):
        if self.end:
            while 1:
                self.screen.fill(BLACK)
                self.draw_text(f"SCORE: {self.score}", 20, WIDTH/2, HEIGHT/2+50)
                self.draw_text("GAME OVER", 50, WIDTH/2, HEIGHT/2)
                pygame.display.update() #flip
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
    def collision(self):
        #colisão corpo a corpo inimigo-heroi
        # for enemy in self.enemies:
        if pygame.sprite.spritecollide(self.ship, self.enemies, False,False):
            self.ship.damage(self)
            hurt_sound.play()
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets,True, True)
        for hit in hits:
            random.choice(expl_sound).play()
            self.score += 50
            self.respawn_enemy()
    def respawn_enemy(self):
        """Cria um inimigo"""
        e = Enemy()
        self.all_sprites.add(e)
        self.enemies.add(e)
    def draw_text( self, text, size, x, y):
        font = pygame.font.Font(game_font, size)
        # font = pygame.font.Font(pygame.font.match_font('arial'), size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
if __name__ ==  '__main__':
    # pygame.mixer.init()
    game = Game()
    game.run()
