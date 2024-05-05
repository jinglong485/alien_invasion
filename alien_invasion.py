import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.clock = pygame.time.Clock()
		self.settings = Settings()
		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")
		#Set the background color. Color is 8bit-RGB
		#set the ship
		self.ship = Ship(self)

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			#Watch for keyboard and mouse events.
			self._check_events()
			self.ship.update()
			self._update_screen()
			self.clock.tick(60)

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
				'''elif event.key == pygame.K_Q:
					sys.exit()
				above is wrong, since only event that relates to key has key
				attirbutes, e.g. mouse movements and clicks are also events,
				but they don't have key as attribute. so to check if q is
				pressed, it should be in _check_keydown_events() 
				'''

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
		pygame.display.flip()


if __name__ == "__main__":
	# Make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()