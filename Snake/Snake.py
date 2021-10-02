import os, sys
import pygame
import random
import numpy as np
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def tail_insert(self, body):
        if self.head == None:
            self.head = body
        else:
            self.tail.prev = body
            body.next = self.tail
        self.tail = body
        self.count += 1

class SnakeHead(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\Snake\snake_head.png')
        self.original = self.image
        screen = pygame.display.get_surface()
        
        self.prev = None
        self.next = None
        self.x = x
        self.y = y
        self.prevx = x
        self.prevy = y
        self.xpos = x*32
        self.ypos = y*32
        self.area = screen.get_rect()
        self.rect.topleft = self.xpos, self.ypos
        self.direction = "none"
        self.collide = 0

    def update(self):
        self.walk()

    def walk(self):
        self.prevx = self.x
        self.prevy = self.y

        if self.direction == "up":
            if self.area.contains(self.rect.move(0, -32)) and not self.body_collision(self.x, self.y-1):
                self.y -= 1
                self.rect = self.rect.move(0, -32)
            else: self.collide = 1
        elif self.direction == "down":
            if self.area.contains(self.rect.move(0, 32)) and not self.body_collision(self.x, self.y+1):
                self.y += 1
                self.rect = self.rect.move(0, 32)
            else: self.collide = 1
        elif self.direction == "left":
            if self.area.contains(self.rect.move(-32, 0)) and not self.body_collision(self.x-1, self.y):
                self.x -= 1
                self.rect = self.rect.move(-32, 0)
            else: self.collide = 1
        elif self.direction == "right":
            if self.area.contains(self.rect.move(32, 0)) and not self.body_collision(self.x+1, self.y):
                self.x += 1
                self.rect = self.rect.move(32, 0)
            else: self.collide = 1
        self.xpos = self.x*32
        self.ypos = self.y*32

    def change_direction(self, direction):
        self.direction = direction

        if self.direction == "up":
            self.image = self.original
        elif self.direction == "down":
            self.image = pygame.transform.flip(self.original, 0, 1)
        elif self.direction == "left":
            self.image = pygame.transform.rotate(self.original, 90)
        elif self.direction == "right":
            self.image = pygame.transform.rotate(self.original, -90)

    def body_collision(self, x, y):
        cur = self.prev
        while cur != None:
            if x == cur.x and y == cur.y:
                return 1
            cur = cur.prev
        return 0

class SnakeBody(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\Snake\snake_body.png')
        self.original = self.image
        screen = pygame.display.get_surface()
        
        self.prev = None
        self.next = None
        self.x = x
        self.y = y
        self.prevx = x
        self.prevy = y
        self.xpos = x*32
        self.ypos = y*32
        self.area = screen.get_rect()
        self.rect.topleft = self.xpos, self.ypos
        self.direction = "none"
        self.collide = 0

    def update(self):
        if self.next.collide == 0: self.walk()
        else: self.collide = 1

    def walk(self):
        self.prevx = self.x
        self.prevy = self.y
        self.x = self.next.prevx
        self.y = self.next.prevy
        self.xpos = self.x*32
        self.ypos = self.y*32
        self.rect.topleft = self.xpos, self.ypos

    def change_direction(self, direction):
        pass

class Food(pygame.sprite.Sprite):
    def __init__(self, list):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\Snake\food.png')
        self.original = self.image
        screen = pygame.display.get_surface()
        
        self.x = 0
        self.y = 0
        self.xpos = 0
        self.ypos = 0
        self.area = screen.get_rect()
        self.rect.topleft = self.xpos, self.ypos
        self.move()
        self.collide = 0
        self.eaten_ = 0
        self.linked_sprites = list

    def update(self):
        self.eaten()

    def eaten(self):
        if self.x == self.linked_sprites.head.x and self.y == self.linked_sprites.head.y:
            self.move()
            self.eaten_ = 1

    def move(self):
        self.x = random.randint(0, 14)
        self.y = random.randint(0, 14)
        self.xpos = self.x*32
        self.ypos = self.y*32
        self.rect.topleft = self.xpos, self.ypos

pygame.init()

screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption("Snake")
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

screen.blit(background, (0, 0))
pygame.display.flip()

head = SnakeHead(7, 7)
linked_sprites = LinkedList()
linked_sprites.tail_insert(head)
food = Food(linked_sprites)
all_sprites = pygame.sprite.RenderPlain((head, food))

clock = pygame.time.Clock()

running = 1
game_start = 0
arrow_pressed = "none"

while running:
    clock.tick(10)

    if linked_sprites.head.collide == 1:
        break
    elif food.eaten_ == 1:
        body = SnakeBody(linked_sprites.tail.x, linked_sprites.tail.y)
        all_sprites.add(body)
        linked_sprites.tail_insert(body)
        food.eaten_ = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = 0
            elif event.key == K_UP:
                arrow_pressed = "up"
            elif event.key == K_DOWN:
                arrow_pressed = "down"
            elif event.key == K_LEFT:
                arrow_pressed = "left"
            elif event.key == K_RIGHT:
                arrow_pressed = "right"

            linked_sprites.head.change_direction(arrow_pressed)

    all_sprites.update()
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()