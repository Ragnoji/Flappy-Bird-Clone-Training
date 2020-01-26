#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random
from c_button import PygButton


class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 708))
        pygame.display.set_caption("Flappy Bird")
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("assets/background.png").convert()
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.wallUp1 = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown1 = pygame.image.load("assets/top.png").convert_alpha()
        self.wallUp2 = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown2 = pygame.image.load("assets/top.png").convert_alpha()
        self.replay = PygButton((99, 438, 299, 512), normal="assets/Replay_n.png", down="assets/Replay_d.png", highlight="assets/Replay_h.png")
        self.replay._propSetVisible(False)
        self.gap = 130
        self.wallx = 400
        self.birdY = 350
        self.wallx2 = 640
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.offset2 = random.randint(-110, 110)
        pygame.init()
        self.dead_s = pygame.mixer.Sound('assets/sfx_die.ogg')
        self.hit_s = pygame.mixer.Sound('assets/sfx_hit.ogg')
        self.point_s = pygame.mixer.Sound('assets/sfx_point.ogg')
        self.fallen_s = pygame.mixer.Sound('assets/sfx_swooshing.ogg')
        self.jump_s = pygame.mixer.Sound('assets/sfx_wing.ogg')
        self.jump_s.set_volume(0.05)
        self.hit_s.set_volume(0.05)
        self.fallen_s.set_volume(0.3)
        self.point_s.set_volume(0.2)
        self.hit = True
        self.c_color = (255, 140, 0)
        self.stop = False
    
    def updateWalls(self):
        self.wallx -= 4
        self.wallx2 -= 4
        if self.wallx < -83:
            self.wallx = 456
            self.offset = random.randint(-110, 110)
        if self.wallx2 < -83:
            self.wallx2 = 456
            self.offset2 = random.randint(-110, 110)
    
    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            if not self.hit:
                if self.bird[1] < 680:
                    self.birdY += self.gravity
                    self.gravity += 0.2
            else:
                if not self.replay._propGetVisible():
                    self.birdY += self.gravity
                    self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx + 3,
                             360 + self.gap - self.offset + 10,
                             self.wallUp1.get_width() - 10,
                             self.wallUp1.get_height())
        downRect = pygame.Rect(self.wallx + 3,
                               -300 - self.gap - self.offset - 10,
                               self.wallDown1.get_width() - 10,
                               self.wallDown1.get_height() + 304)
        upRect2 = pygame.Rect(self.wallx2 + 3,
                             360 + self.gap - self.offset2 + 10,
                             self.wallUp2.get_width() - 10,
                             self.wallUp2.get_height())
        downRect2 = pygame.Rect(self.wallx2 + 3,
                               -300 - self.gap - self.offset2 - 10,
                               self.wallDown2.get_width() - 10,
                               self.wallDown2.get_height() + 304)
        if (upRect.colliderect(self.bird) or upRect2.colliderect(self.bird)) and not(self.dead) and self.hit:
            self.dead = True
            self.replay._propSetVisible(True)
            if self.hit == True:
                self.jump = 17
                self.gravity = 5
                self.jumpSpeed = 10
                self.jump_s.stop()
                self.jump_s.play()
                self.jump_s.stop()
                self.hit_s.play()
                self.hit = False
        if (downRect.colliderect(self.bird) or downRect2.colliderect(self.bird)) and not(self.dead) and self.hit:
            self.dead = True
            self.replay._propSetVisible(True)
            if self.hit == True:
                self.jump = 17
                self.gravity = 5
                self.jumpSpeed = 10
                self.jump_s.stop()
                self.jump_s.play()
                self.jump_s.stop()
                self.jump_s.stop()
                self.hit_s.play()
                self.hit = False
        if self.bird[1] > 720:
            if not self.dead:
                self.fallen_s.play()
            self.dead = True
            self.replay._propSetVisible(True)
        if (self.wallx == -4 or self.wallx2 == -4) and not(self.dead):
            self.counter += 1
            if self.counter % 5 == 0:
                self.jump_s.stop()
                self.point_s.play()
                if self.counter % 10 == 0:
                    self.c_color = tuple((int(x) + 20) % 256 for x in self.c_color)
        self.replay.draw(self.screen)

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Times New Roman", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.stop = True if not(self.stop) else False
                elif self.dead and not self.stop and event.type in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) and self.replay._propGetVisible():
                    react = self.replay.handleEvent(event)
                    if 'click' in react:
                        self.bird[1] = 50
                        self.birdY = 50
                        self.dead = False
                        self.hit = True
                        self.counter = 0
                        self.wallx = 400
                        self.wallx2 = 700
                        self.offset = random.randint(-110, 110)
                        self.offset2 = random.randint(-110, 110)
                        self.gravity = 5
                        self.c_color = (255, 140, 0)
                elif(not(self.stop) and (event.type == pygame.KEYDOWN
                                         or event.type == pygame.MOUSEBUTTONDOWN)
                     and not self.dead):
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10
                    self.jump_s.stop()
                    self.jump_s.play()

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp1,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown1,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(self.wallUp2,
                             (self.wallx2, 360 + self.gap - self.offset2))
            self.screen.blit(self.wallDown1,
                             (self.wallx2, 0 - self.gap - self.offset2))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         self.c_color),
                             (200, 50))
            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            if not self.dead:
                if self.jump < 10:
                    self.sprite = 0
                if not(self.stop):
                    self.updateWalls()
            if not(self.stop):
                self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
                self.birdUpdate()
                pygame.display.update()
                self.replay._update()
                self.replay.draw(self.screen)


if __name__ == "__main__":
    FlappyBird().run()
