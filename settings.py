class Settings:
	"""A class to store all setting for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's settings."""
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		# I like Blue sky for Haiku
		self.bg_color = (0, 128, 220)
		self.ship_speed = 5
		# Bullet settings
		self.bullet_speed = 10.0
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 3
		#Alien settings
		self.alien_speed = 1.0
		self.fleet_drop_speed = 10
		#fleet_direction of 1 reprersents right, -1 means left
		self.fleet_direction = 1