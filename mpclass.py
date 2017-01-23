# -*- coding: utf-8 -*-
from multiprocessing import Value

class MPCounter(object):
	def __init__(self):
		self.val = Value('i', 0)
	
	def increment(self, n=1):
		with self.val.get_lock():
			self.val.value += n
	
	@property
	def value(self):
		return self.val.value