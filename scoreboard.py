import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
	"""A class to report scoring information."""

	def __init__(self, ai_game):
		"""Initialize scorekeeing attributes"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats
		self.ai_game = ai_game

		# Font settings for scoring information
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)

		# Prepare the initial score image.
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		"""Turn the score into a redered image"""
		rounded_score = round(self.stats.score,-1)
		score_str = f"{rounded_score:,}"
		self.score_image = self.font.render(score_str, True,
									  self.text_color, self.settings.bg_color)
		
		# Display the score at the top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def show_score(self):
		"""Draw score to the screen"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_image_rect)
		self.ships.draw(self.screen)

	def prep_high_score(self):
		high_score = round(self.stats.high_score, -1)
		high_score_str = f"{high_score:,}"
		self.high_score_image = self.font.render(high_score_str, True,
										   self.text_color, self.settings.bg_color)
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def check_high_score(self):
		"""Check to see if there's a new score"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def prep_level(self):
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True,
									  self.text_color, self.settings.bg_color)
		self.level_image_rect = self.level_image.get_rect()
		self.level_image_rect.top = self.score_rect.top
		self.level_image_rect.left = self.screen_rect.left + 20

	def prep_ships(self):
		self.ships = Group()

		for ship_num in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.top = self.level_image_rect.bottom
			ship.rect.x = 10 + ship_num * ship.rect.width
			self.ships.add(ship)