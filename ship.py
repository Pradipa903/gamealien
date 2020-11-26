import pygame

class Ship:

	def __init__(self, AlienWorld):
		self.screen = AlienWorld.screen
		self.screen_rect = AlienWorld.screen.get_rect()

		self.settings =  AlienWorld.my_settings

		self.image = pygame.image.load("img/ship.PNG")
		self.rect = self.image.get_rect()

		self.re_position_ship()

		#Status Movement
		self.moving_up = False
		self.moving_down = False
		self.moving_right = False
		self.moving_left = False

	def update(self):
		if self.moving_up and self.rect.top > 0:
			#self.rect.y -= 1
			self.y -= self.settings.ship_speed
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			#self.rect.y += 1
			self.y += self.settings.ship_speed
		if self.moving_right and self.rect.right < self.screen_rect.right:
			#self.rect.x += 1
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			#self.rect.x -= 1
			self.x -= self.settings.ship_speed

		self.rect.x = self.x
		self.rect.y = self.y
	
	def re_position_ship(self):
		self.rect.midbottom = self.screen_rect.midbottom

		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

	def blit_ship(self):
		#update frame dalam game every location
		self.screen.blit(self.image, self.rect)
