import math
from random import randint
import pygame
import sys

pygame.init()
state = 1

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 700
fps = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Entropy')
clock = pygame.time.Clock()

def round_to_one(num):
    if 0 < num < 1:
        num = 1
    elif -1 < num < 0:
        num = -1
    return num


def momentum(mass, speed):
    return mass * speed


class Ball(pygame.sprite.Sprite):

    def __init__(self, initx, inity, speed, angle, radius, c, num):
        pygame.sprite.Sprite.__init__(self)
        self.initx, self.inity = initx, inity
        self.speed = speed
        self.angle = angle
        self.radius = radius
        self.c = c
        self.num = num
        self.spdx = speed * math.sin(math.radians(180 - angle))
        self.spdy = speed * math.cos(math.radians(180 - angle))
        self.mass = math.pi * radius**2
        self.lastwall = None
        self.lastcld = None
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(initx, inity))
        
    def calc_speed(self, other):
        if self.lastcld != other.num:
            old_spdx, old_spdy = self.spdx, self.spdy
            self.spdx = (self.mass - other.mass) / (self.mass + other.mass) * self.spdx + 2 * other.mass / (self.mass + other.mass) * other.spdx
            self.spdy = (self.mass - other.mass) / (self.mass + other.mass) * self.spdy + 2 * other.mass / (self.mass + other.mass) * other.spdy
            self.spdx *= 0.99
            self.spdy *= 0.99
            self.rect.x += self.spdx
            self.rect.y += self.spdy
            self.lastcld = other.num
            self.lastwall = None
            other.spdx = 2 * self.mass / (self.mass + other.mass) * old_spdx + (other.mass - self.mass) / (self.mass + other.mass) * other.spdx
            other.spdy = 2 * self.mass / (self.mass + other.mass) * old_spdy + (other.mass - self.mass) / (self.mass + other.mass) * other.spdy
            other.spdx *= 0.99
            other.spdy *= 0.99
            other.rect.x += other.spdx
            other.rect.y += other.spdy
            other.lastcld = self.num
            other.lastwall = None
            
    def move(self):
        if self.rect.left <= 0 and self.lastwall != 'left':
            self.spdx *= -0.99
            self.spdx = round_to_one(self.spdx)
            self.rect.x += self.spdx
            self.rect.y += self.spdy
            self.lastwall = 'left'
            self.lastcld = None
        elif self.rect.right >= SCREEN_WIDTH and self.lastwall != 'right':
            self.spdx *= -0.99
            self.spdx = round_to_one(self.spdx)
            self.rect.x += self.spdx
            self.rect.y += self.spdy
            self.lastwall = 'right'
            self.lastcld = None
        elif self.rect.top <= 0 and self.lastwall != 'top':
            self.spdy *= -0.99
            self.spdy = round_to_one(self.spdy)
            self.rect.x += self.spdx
            self.rect.y += self.spdy
            self.lastwall = 'top'
            self.lastcld = None
        elif self.rect.bottom >= SCREEN_HEIGHT and self.lastwall != 'bottom':
            self.spdy *= -0.99
            self.spdy = round_to_one(self.spdy)
            self.rect.x += self.spdx
            self.rect.y += self.spdy
            self.lastwall = 'bottom'
            self.lastcld = None
        else:
            self.rect.x += self.spdx
            self.rect.y += self.spdy
        pygame.draw.circle(self.image, self.c, (self.radius, self.radius), self.radius)
        screen.blit(self.image, (self.rect.x, self.rect.y))


ball_list = []
num_balls = randint(5, 20)

for i in range(20):
    ball_list.append(Ball(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT), randint(5, 20), randint(15, 345), randint(10, 40), (randint(0, 255), randint(0, 255), randint(0, 255)), i))


while True:
    
    if state == 1:
    
        screen.fill((0, 0, 0))

        for balls in ball_list:
            passed = True
            balls.move()
            for others in ball_list[:ball_list.index(balls)] + ball_list[ball_list.index(balls)+1:]:
                if pygame.sprite.collide_circle(others, balls):
                    balls.calc_speed(others)          

        clock.tick(fps)
        pygame.display.update()

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == 1:
                    state = 0
                elif state == 0:
                    state = 1
