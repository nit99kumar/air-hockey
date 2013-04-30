import os, sys
import pygame
from pygame.locals import *

size = iWidth, iHeight = 1280, 720
iPosBat = iHeight * 0.9

if not pygame.font: print 'Warning!fonts disabled'
if not pygame.mixer: print 'Warning!sound disabled'

def load_image(name, colorkey=None):
	fullname = os.path.join(name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error:
		print 'cannot load image', fullname
		raise SystemExit
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	
	return image, image.get_rect()
	
def load_sound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound
	fullname = os.path.join(name)
	try:
		sound = pygame.mixer.sound(fullname)
	except pygame.error:
		print 'cannot load sound ', fullname
		raise SystemExit
	return sound
	
class Bat(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('bat.jpg', -1)
		
	def update(self):
		#move the bat based on mouse position
		pos = pygame.mouse.get_pos()
		self.rect.center = pos[0], iPosBat
	
	def bounce(self, target):
		if self.rect.colliderect(target.rect):
			return self.rect.colliderect(target.rect)

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('ball.png', -1)
		self.rect.topleft = 10, 10
		self.move = [19,19]
	
	def update(self):
		self.random_walk()
			
	def random_walk(self):
		newpos = self.rect.move(self.move)
		if self.rect.left < 0 or self.rect.right > iWidth:
			self.move[0] = -self.move[0]
		if self.rect.top < 0 or self.rect.bottom > iHeight:
			self.move[1] = -self.move[1]
		newpos = self.rect.move(self.move)
		self.rect = newpos
	
	def bounce(self):
		self.move[1] = -self.move[1]
		newpos = self.rect.move(self.move)
		self.rect = newpos
		
def main():
	#initialise
	pygame.init()
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption('Air Hockey')
	pygame.mouse.set_visible(0)
	
	#create the background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	
	#display the background
	screen.blit(background, (0,0))
	pygame.display.flip()
	
	#prepare game objects
	clock = pygame.time.Clock()
	ball = Ball()
	bat  = Bat()
	allsprites = pygame.sprite.RenderPlain((ball, bat))
	
	#main loop
	flag = True
	while flag:
		clock.tick(60)
		
		#handling input events
		for event in pygame.event.get():
			if event.type == QUIT: 
				flag = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				flag = False
			#elif event.type == MOUSEBUTTONDOWN: 
			if bat.bounce(ball):
				ball.bounce()
			
		allsprites.update()
		
		#draw everything
		screen.blit(background, (0,0))
		allsprites.draw(screen)
		pygame.display.flip()
	
	pygame.quit()

if __name__ == '__main__': main()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
