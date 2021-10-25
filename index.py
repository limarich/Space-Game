import pygame,sys
import pygame,sys
from pygame.locals import *
class Character:
    def __init__(self, width,height,position=(0,0), color=(0,0,0)):
        self.height = height
        self.width = width
        self.surface = pygame.Surface((width,height))
        self.color = color
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        self.rect[0], self.rect[1] = position[0], position[1]
    def change_color(self, color):
        self.color = color
        self.surface.fill(color)
class Hero(Character):
    def __init__(self,width,height,position,color):
        super().__init__(width,height,position,color)
    def shoot(self):
        shot = Shot([self.rect[0],self.rect[1]])
        return shot
class Shot:
    def __init__(self,position,direction=1,width = 10, height=20, color=(255,255,0), speed=8):
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.surface = pygame.Surface((width,height))
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        self.direction = direction

    def update(self):
        self.position[1] = self.position[1] - self.speed
        if self.position[1] < 0 and self.direction == 1: #direção jogador
            del self
def main():
    width,height = 640,480
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("!!!Space Game!!!")
    clock = pygame.time.Clock()
    color1, color2 = (255,0,0),(255,255,0)

    hero = Hero(40,40,((width/2),(height-40)),color1)
    enemy = Character(40,40,(width/2,0),color2)
    # shoot = Shoot(10,20,(hero.rect[0]+20, height-60))
    speed = [10,0]
    black = [0,0,0]
    click = 1
    shoots = []
    i = 0
    # shoots.append(Shoot(10,20,(hero.rect[0]+20, height-60)))
    # print(hero.position)
    while 1:
        keys = pygame.key.get_pressed()
        # pygame.time.set_timer(USEREVENT+1,700) lazer hehe
        # if tempo % x == 0:
        # shoots.append(hero.shoot())

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if click == 1:
                    hero.change_color(color1)
                    enemy.change_color(color2)
                else:
                    hero.change_color(color2)
                    enemy.change_color(color1)
                click = -click
        if keys[K_LEFT] or keys[K_a]:
            if(hero.rect.left-10 > 0):
                hero.rect = hero.rect.move((-10,0))
        if keys[K_RIGHT] or keys[K_d]:
            if(hero.rect.left+10 < width-40):
                hero.rect = hero.rect.move((+10,0))
        if keys[K_SPACE]:
           shoots.append(hero.shoot())

        if enemy.rect.right > width or enemy.rect.left < 0:
            speed[0] =  -speed[0] 
        # if shoots[0].rect[1] <  0:
            # print(len(shoots))
            # shoots.pop(0)
            # print(len(shoots))
        enemy.rect = enemy.rect.move(speed)
        # for shoot in shoots:
        #     shoot.rect = shoot.rect.move(0,-10)
        clock.tick(30)
        screen.fill(black)
        screen.blit(hero.surface, hero.rect)
        screen.blit(enemy.surface, enemy.rect)
        for shoot in shoots:
            screen.blit(shoot.surface, shoot.position)
            # print(shoot.rect[1])
        for shoot in shoots:
            shoot.update()        
        pygame.display.flip()
main()
