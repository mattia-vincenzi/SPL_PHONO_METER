import time
import logging
import datetime
import sys
import signal
import subprocess
import shlex

class SplReader:
	def setup(self, seconds):
		"""
			Function used to setup and return logger with specified format.
		"""
		self.name = "phonometer-{}.csv".format(str(datetime.date.today()))
		self.file_logger = logging.basicConfig(
        		filename = self.name,
        		format = "%(asctime)s %(message)s", # Format date_time data.
        		level = logging.INFO)
		
		print("Printing data on {}".format(self.name))

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
		"""
			Main loop of program, that read analog input for n seconds.
		"""
		while self.is_alive:
			raw = float(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
			scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
			# Obtain millivolt read from analog input..
			voltage = raw * scale
			# Convert millivolt in dbSPL using: 10mV = 1dB.
			dbSPL = voltage / 10.0
			#print(dbSPL)
			self.file_logger.info(dbSPL)
			time.sleep(1)

	def send_to_server(self):
		"""
			Send data to remote server.
		"""
		#print("scp -i ~/Desktop/phonometer {} mattia.vincenzi2@studio.unibo.it@isi-studio8bis.csr.unibo.it:~/gathered_data/phonometer/".format(self.name))
		#bash_command = "scp -i ~/Desktop/phonometer {} mattia.vincenzi2@studio.unibo.it@isi-studio8bis.csr.unibo.it:~/gathered_data/phonometer/".format(self.name)
		#process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
		#output, error = process.communicate()
		subprocess.call(shlex.split('./file_transfer.sh {}'.format(self.name)))

# Command line params
if len(sys.argv) != 2:
	raise Exception("Usage: python3 script.py seconds")
else:
	name, seconds = sys.argv

spl_meter = SplReader()
spl_meter.setup(seconds)
spl_meter.MainLoop()

# Send data to remote server.
spl_meter.send_to_server()

print("Program terminated.")
