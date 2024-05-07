import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.clock = pygame.time.Clock()
		self.settings = Settings()
		self._init_screen()
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()
		# Start Alien Invasion in an active state.
		self.game_active = False
		self.play_button = Button(self, "Play")

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			#Watch for keyboard and mouse events.
			self._check_events()
			if self.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()
			self.clock.tick(60)

	def _init_screen(self):
		if self.settings.screen_mode == 0:
			self.screen = pygame.display.set_mode(
				size=(self.settings.screen_width, self.settings.screen_height))
			pygame.display.set_caption("Alien Invasion")
		if self.settings.screen_mode == 1:
			self.screen = pygame.display.set_mode(size=(0, 0),
											flags=pygame.FULLSCREEN)
			self.settings.screen_height = self.screen.get_rect().height
			self.settings.screen_width = self.screen.get_rect().width

	def _check_events(self):
		"""Respond to keypresses and mouse events"""
		for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)
				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)
				#elif event.key == pygame.K_Q:
				#	sys.exit()
				#above is wrong, since only event that relates to key has key
				#attirbutes, e.g. mouse movements and clicks are also events,
				#but they don't have key as attribute. so to check if q is
				#pressed, it should be in _check_keydown_events() '''
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()
					self._check_play_button(mouse_pos)
	
	def _check_play_button(self, mouse_pos):
		"""Start a new game when the play clicks paly."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.game_active:
			self.settings.initialize_dynamic_settings()
			#Hide the mouse cursor
			pygame.mouse.set_visible(False)
			self.stats.reset_stats()
			self.sb.prep_score()
			self.sb.prep_level()
			self.game_active = True
			# get rid of any remaining bullets and aliens
			self.bullets.empty()
			self.aliens.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

	def _check_keydown_events(self, event):
		"""Respond to keypresses"""
		if event.key == pygame.K_RIGHT:
			# move the ship to the right
			#self.ship.rect.x += 1
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE and self.game_active:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		"""Respond to key releases"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _update_screen(self):
		"""update images on the screen, and flip to the new screen"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet() 
		self.aliens.draw(self.screen)
		self.sb.show_score()
		# Draw the play button if the game is inactive
		if not self.game_active:
			self.play_button.draw_button()
		pygame.display.flip()

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullet_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets"""
		# Update bullet positions.
		self.bullets.update()
		#python expect the list stays the same length as the loop is runing
		#copy of the list for the loop is necessary
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		#the commented chaged bullet behavier, instead stop firing, the
		# earliest fired bullet disaprears. make the total bullets less
		# than self.setting.bullet_allowed
		#if len(self.bullets) > self.settings.bullet_allowed:
		#	self.bullets.remove(self.bullets.sprites().pop(0))
		# Check for any bullets that have hit aliens
		#   If so, get rid of the bullet and the alien
		self._check_bullet_alien_collisions()
		# this is refactored into a function

	def _check_bullet_alien_collisions(self):	
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True
		) # if False, True then panatrating pullet!
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			self.stats.level += 1
			self.sb.prep_level()
		if collisions:
			#print(collisions.values())
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

	def _create_fleet(self):
		"""Create the fleet of aliens"""
		# Make an alien.
		# Create an alien and keep adding aliens until there's no room left.
		# Spacing between aliens is one alien width and one alien height
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		del alien #release menory

		current_x, current_y = alien_width, alien_height
		while current_x < (self.settings.screen_width - 2 * alien_width):
			while current_y <(self.settings.screen_height - 5 * alien_height):
				self._create_alien(current_x, current_y)
				current_y += 2 * alien_height
			current_y = alien_height
			current_x += 2 * alien_width
				
	
	def _create_alien(self, x_position, y_position):
		new_alien = Alien(self)
		new_alien.x = x_position # precise position float
		new_alien.rect.x = x_position # rect position int
		new_alien.rect.y = y_position
		self.aliens.add(new_alien)

	def _update_aliens(self):
		"""Update the positions of all aliens in the fleet."""
		self._check_fleet_edges()
		self.aliens.update()
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		# Look for aliens hitting the bottom fo the screen
		self._check_aliens_bottom()

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edge():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""Respond to the ship being hit by an alien"""
		if self.stats.ships_left > 0:
			# Decrement ships_left
			self.stats.ships_left -= 1
			# get rid of any remaining bullets and aliens
			self.bullets.empty()
			self.aliens.empty()
			# create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()
			# Pause 0.5 second
			sleep(0.5)
		else:
			self.game_active = False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen."""
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= self.settings.screen_height:
				#Treat this same as if the ship got hit.
				self._ship_hit()
				break


if __name__ == "__main__":
	# Make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()