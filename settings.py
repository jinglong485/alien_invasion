class Settings:
	"""A class to store all setting for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's settings."""
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		# I like Blue sky for Haiku
		self.bg_color = (0, 128, 220)
		self.ship_speed = 1.5