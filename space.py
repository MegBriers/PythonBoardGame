#!/usr/bin/env python
 
# A simple effect of sliding stars to create a deep space sensation.
# by Silveira Neto <me@silveiraneto.net>
# Free under the terms of GPLv3 license
# See http://silveiraneto.net/2009/08/12/pygame-simple-space-effect/
 
import os,sys,random
import pygame
from pygame.locals import *
 
# Constants 
N = 200
SCREEN_W, SCREEN_H = (640, 480)
 
def mainwinner():
	# basic start
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
	pygame.display.set_caption('You are the winner!')
 
	# create background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
 
	# generate N stars
	stars = [
		[random.randint(0, SCREEN_W),random.randint(0, SCREEN_H)]
		for x in range(N)
	]
 
	# main loop
	clock = pygame.time.Clock()
	while 1:
		clock.tick(22)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return
		background.fill((0,0,128))
		for star in stars:
			pygame.draw.line(background,
				(255, 255, 255), (star[0], star[1]), (star[0], star[1]))
			star[0] = star[0] - 1
			if star[0] < 0:
				star[0] = SCREEN_W
				star[1] = random.randint(0, SCREEN_H)
		screen.blit(background, (0,0))
		pygame.display.flip()
 
if __name__ == '__main__': mainwinner()
