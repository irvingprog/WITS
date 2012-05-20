import time

class Timer():
	"""docstring for Timer"""
	def __init__(self):
		self.running = False
		self.offset = 0

	def time(self):
		if self.running:
			self.__time = (time.clock() - self.start())
			return self.__time
		return self.__time

	def start(self):
		if not self.running:
			self.running=True
			self.offset = time.clock();

		return self.offset

	def stop(self):
		self.running = False