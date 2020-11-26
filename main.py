import pygame
import sys
import random
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats

class AlienWorld:

	def __init__(self):
		pygame.init()
		self.my_settings = Settings()

		self.error = False
		self.screen = pygame.display.set_mode([self.my_settings.window_width, self.my_settings.window_height])
		#self.screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN)
		self.title = pygame.display.set_caption("Game ALIEN")
		#self.bg_color = self.my_settings.bg_color
		self.background = self.my_settings.background.convert()

		self.my_ship = Ship(self)
		self.bullets = pygame.sprite.Group() #container for bullet
		self.alien_army = pygame.sprite.Group()
		self.my_stars = pygame.sprite.Group()

		self.my_stats = GameStats(self)

		self.create_alien_army()
		self.create_my_stars()

	def run_game(self):
		while not self.error:
			self.check_events() #refactoring
			self.update_ship()
			self.update_bullet()
			self.update_alien()
			self.update_frame() #refactoring
	
	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
					#sys.exit()
					self.error = True
			elif event.type == pygame.KEYDOWN:
					self.check_keydown_event(event) #refactoring

			elif event.type == pygame.KEYUP:
					self.check_keyup_event(event) #refactoring

	

	def check_keydown_event(self, event):
		if event.key == pygame.K_w: #forward
			self.my_ship.moving_up = True
		elif event.key == pygame.K_s: #backward
			self.my_ship.moving_down = True
		elif event.key == pygame.K_d: #right
			self.my_ship.moving_right = True
		elif event.key == pygame.K_a: #left
			self.my_ship.moving_left = True
		elif event.key == pygame.K_q: #Quit
			self.error = True
		elif event.key == pygame.K_SPACE: #Fire!
			self.fire_bullet()
		elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_RCTRL:
			self.screen = pygame.display.set_mode([self.my_settings.window_width, self.my_settings.window_height])
		elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_SHIFT:
			#self.screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN)
			pass
			
	def check_keyup_event(self, event):
		if event.key == pygame.K_w:
			self.my_ship.moving_up = False
		elif event.key == pygame.K_s: 
			self.my_ship.moving_down = False
		elif event.key == pygame.K_d:
			self.my_ship.moving_right = False
		elif event.key == pygame.K_a: 
			self.my_ship.moving_left = False

	
	def fire_bullet(self):
		if len(self.bullets) < self.my_settings.bullet_capacity:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def update_ship(self):
		self.my_ship.update() #piloting ship

		if pygame.sprite.spritecollideany(self.my_ship, self.alien_army):
			#print("Kapal Menabrak Alien")
			self.ship_hit()

	def ship_hit(self):
		self.my_stats.ship_life -= 1

		self.alien_army.empty()
		self.bullets.empty()

		self.create_alien_army()
		self.my_ship.re_position_ship() #set ulang posisi ship

		sleep(0.5)

	def update_bullet(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		#print(len(self.bullets))

		self.check_bullet_alien_collision()


	def check_bullet_alien_collision(self):
		collisions = pygame.sprite.groupcollide(self.alien_army, self.bullets, True, True)
		#collisions = pygame.sprite.groupcollide(self.alien_army, self.bullets, False, True)
		#for hitalien in collisions:
		#	#print(alien.life)
			#hitalien.life -= 1
			#if hitalien.life == 0:
				#self.alien_army.remove(hitalien)

		if len(self.alien_army) == 0:
			self.bullets.empty()
			self.create_alien_army()		

	def create_alien(self, each_alien, every_row):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + (2 * alien_width * each_alien) 
		alien.rect.x = alien.x
		alien.rect.y = alien_height + (2 * alien_height * every_row)
		self.alien_army.add(alien)

	def create_alien_army(self):
		alien = Alien(self)
		alien_width, alien_width = alien.rect.size
		available_space_for_alien = self.my_settings.window_width - (2*alien_width)
		number_of_alien = available_space_for_alien // (2*alien_width)

		alien_height = alien.rect.height
		ship_p1_height = self.my_ship.rect.height
		available_space_for_row = self.my_settings.window_height - (3*alien_height) - ship_p1_height
		number_of_row = available_space_for_row // (2*alien_height)

		for every_row in range (number_of_row-1):
			for each_alien in range(number_of_alien-1):
				self.create_alien(each_alien, every_row)

	def update_alien(self):
		self.check_alien_army()
		self.alien_army.update()

	def check_alien_army(self):
		for alien in self.alien_army.sprites():
			if alien.check_edges():
				self.change_direction_alien_army()
				break

	def change_direction_alien_army(self):
		for alien in self.alien_army.sprites():
			alien.rect.y += self.my_settings.alien_drop_speed
		self.my_settings.alien_direction *= -1

	def create_star(self, pos_x, pos_y):
		star = Star(self)
		star.rect.x, star.rect.y = pos_x, pos_y
		self.my_stars.add(star)
	
	def create_my_stars(self):
		star = Star(self)
		star_width, star_height = star.rect.size
		number_of_stars = (self.my_settings.window_width * self.my_settings.window_height)//(star_width*star_height)

		for each_star in range(number_of_stars//5):
			pos_x = random.randint(0, self.my_settings.window_width)
			pos_y = random.randint(0, self.my_settings.window_height)
			self.create_star(pos_x, pos_y)
				
	def update_frame(self):
		#self.screen.fill(self.bg_color)
		self.screen.blit(self.background, [0, 0])
		self.my_stars.draw(self.screen)

		self.my_ship.blit_ship()


		for bullet in self.bullets.sprites():
			bullet.draw()
		self.alien_army.draw(self.screen)
		
		pygame.display.flip()

Game_ALIEN = AlienWorld()
Game_ALIEN.run_game()