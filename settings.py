class Settings:
	"""A class to store all setting for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's settings."""
		#Screen settings
		self.screen_mode = 1 #0 is smalll window, 1 is fullscreen
		self.screen_width = 1200
		self.screen_height = 800
		# I like Blue sky for Haiku
		self.bg_color = (0, 128, 220)
		self.ship_speed = 5
		self.ship_limit = 3
		# Bullet settings
		self.bullet_speed = 10.0
		self.bullet_width = 5
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 3
		#Alien settings
		self.alien_speed = 2
		self.fleet_drop_speed = 5
		#fleet_direction of 1 reprersents right, -1 means left
		self.fleet_direction = 1
		# How quickly the game speeds up
		self.speedup_scale = 1.05
		# How quickly the alien point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed = 5
		self.bullet_speed = 10
		self.alien_speed = 2
		self.fleet_direction = 1
		self.alien_points = 50

	def increase_speed(self):
		"""Increase speed settings."""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		print(self.alien_points)
	
