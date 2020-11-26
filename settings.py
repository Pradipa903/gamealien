import pygame

class Settings:

	def __init__(self):
		#Arena Settings
		self.window_width = 800
		self.window_height = 600
		#self.bg_color = (246, 153, 66)
		self.background = pygame.image.load("img/space.PNG")

		#Ship Settings
		self.ship_speed = 10
		self.ship_life = 2

		#Bullet settings
		self.bullet_speed = 5
		self.bullet_width = 2
		self.bullet_height = 10
		self.bullet_color = (60, 242, 187)
		self.bullet_capacity = 3


		#Alien Settings
		self.alien_speed = 1.0
		self.alien_drop_speed = 30
		self.alien_direction = 1 # 1 ke kanan -1 untuk ke kiri