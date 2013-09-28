import time

class Timer():
	"""Module time for Games"""
	def __init__(self):
		self.running = False
		self.offset = 0

	def start(self):
		"""Start timer"""
		if not self.running:
			self.running=True
			self.offset = time.clock();

		return self.offset

	def time(self):
		"""Return current time"""
		if self.running:
			self.__time = (time.clock() - self.start())
			return self.__time
		return self.__time


	def stop(self):
		"""Stop timer"""
		self.running = False