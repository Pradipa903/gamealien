
class GameStats:

	def __init__(self, AlienWorld):
		self.setting = AlienWorld.my_settings
		self.reset_stats()

	def reset_stats(self):
		self.ship_life = self.setting.ship_life