import time
import logging
import datetime
import sys
import signal
from functools import partial

class SplReader:
	def setup(self, seconds):
		"""
			Function used to setup and return logger with specified format.
		"""
		name = "phonometer-{}.csv".format(str(datetime.date.today()))
		self.file_logger = logging.basicConfig(
        		filename = name,
        		format = "%(asctime)s %(message)s", # Format date_time data.
        		level = logging.INFO)
		
		print("Printing data on {}".format(name))

		self.file_logger = logging.getLogger(__name__) # Get personalized logger.

		# Set handler for timer signal.
		signal.signal(signal.SIGALRM, self.sigalrm_handler)

		# Set seconds after then generate signal
		signal.setitimer(signal.ITIMER_REAL, int(seconds))

		self.is_alive = True


	def sigalrm_handler(self, signum, frame):
		"""
        		SEGALARM Handler.
		"""
		self.is_alive = False

	def MainLoop(self):
		while self.is_alive:
			raw = float(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
			scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
			voltage = raw * scale
			dbSPL = voltage / 10.0  
			self.file_logger.info(dbSPL)
			time.sleep(1)

# Command line params
if len(sys.argv) != 2:
	raise Exception("Usage: python3 script.py seconds")
else:
	name, seconds = sys.argv

spl_meter = SplReader()
spl_meter.setup(seconds)
spl_meter.MainLoop()

print("Program terminated.")
