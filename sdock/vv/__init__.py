import os,sys
from abc import ABC, abstractmethod
import vagrant_v0,vagrant_v1,vagrant_v2

def datetime_valid(dt_str):
	import datetime
	try:
		datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
	except:
		return False
	return True

class Provider(ABC):
	@abstractmethod
	def install(self):
		pass

	@abstractmethod
	def uninstall(self):
		pass

	@abstractmethod
	def set_name(self, string):
		pass

	@abstractmethod
	def set_date(self, string):
		pass

	@abstractmethod
	def disable_network(self):
		pass

	@abstractmethod
	def disable_timesync(self):
		pass

	@abstractmethod
	def on(self):
		pass

	@abstractmethod
	def off(self):
		pass

	def __enter__(self):
		self.on()
		return self

	def __exit__(self, a=None, b=None, c=None):
		self.off()
	
	def inverse(self):
		class stub(object):
			def __init__(self, on_func, off_func):
				self.on_func = on_func
				self.off_func = off_func

			def __enter__(self):
				self.off_func()

			def __exit__(self, a=None, b=None, c=None):
				self.on_func()

		return stub(self.on, self.off)

vagrant = vagrant_v2.vagrant