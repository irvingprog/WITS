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
			self._time = (time.clock() - self.start())
		else:
			self._time = None
		return self._time		

	def resume(self):
		self.running = True

	def stop(self):
		"""Stop timer"""
		self.running = False