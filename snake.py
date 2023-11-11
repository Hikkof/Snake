import pygame
import random


RED = (255, 0, 50)
GREEN = (0, 128, 0)


class Snake(object):  # to control the snake use w, a, s, d keys
    def __init__(self, game):
        self.game = game
        self.size = 1

        self.pos = pygame.math.Vector2(self.game.width*0.475, self.game.height*0.475)
        self.vel = pygame.math.Vector2(0, -self.game.height/20)
        self.body = [self.pos]
        self.fruit_pos = self.fruit()

    def tick(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w] and self.vel != pygame.math.Vector2(0, self.game.height/20):
            self.vel = pygame.math.Vector2(0, -self.game.height/20)
        if pressed[pygame.K_s] and self.vel != pygame.math.Vector2(0, -self.game.height/20):
            self.vel = pygame.math.Vector2(0, self.game.height/20)
        if pressed[pygame.K_d] and self.vel != pygame.math.Vector2(-self.game.width/20, 0):
            self.vel = pygame.math.Vector2(self.game.width/20, 0)
        if pressed[pygame.K_a] and self.vel != pygame.math.Vector2(self.game.width/20, 0):
            self.vel = pygame.math.Vector2(-self.game.width/20, 0)
        last_x, last_y = self.body[-1].x, self.body[-1].y
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].x, self.body[i].y = self.body[i-1].x, self.body[i-1].y
        self.pos += self.vel

        self.collision()
        self.eat(last_x, last_y)

    def collision(self):
        if self.pos.x < 0 or self.pos.x+self.game.width/20 > self.game.width:
            self.game.game_over()
        if self.pos.y < 0 or self.pos.y+self.game.height/20 > self.game.height:
            self.game.game_over()

        for i in self.body[1:]:
            if self.pos.x == i.x and self.pos.y == i.y:
                self.game.game_over()

    def draw(self):
        for i in self.body:
            rect = pygame.Rect(i.x, i.y, self.game.width / 20, self.game.height / 20)
            pygame.draw.rect(self.game.screen, GREEN, rect)
        rect = pygame.Rect(self.fruit_pos.x, self.fruit_pos.y, self.game.width / 20, self.game.height / 20)
        pygame.draw.rect(self.game.screen, RED, rect)

    def eat(self, last_x, last_y):
        if self.pos.x == self.fruit_pos.x and self.pos.y == self.fruit_pos.y:
            self.size += 1
            self.body.append(pygame.math.Vector2(last_x, last_y))
            self.fruit_pos = pygame.math.Vector2(self.fruit())

    def fruit(self):
        fruit = pygame.math.Vector2(random.randrange(0, self.game.width - self.game.width/20, self.game.width/20) + self.game.width/40,
                                    random.randrange(0, self.game.height - self.game.height/20, self.game.height/20) + self.game.width/40)
        while fruit in self.body:
            fruit = pygame.math.Vector2(random.randrange(0, self.game.width - self.game.width / 20,
                                                         self.game.width / 20) + self.game.width / 40,
                                        random.randrange(0, self.game.height - self.game.height / 20,
                                                         self.game.height / 20) + self.game.width / 40)
        return fruit
