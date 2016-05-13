
import time
import pigpio
# import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

class RadCounter:
	
	def __init__(self, pi, gpio, maxcount):
		self._pi = pi
		self._gpio = gpio
		self._maxCount = maxcount
				
		pi.set_mode(self._gpio, pigpio.INPUT)
	
	def start(self):
		"""
		Prepare members for measurement and setup callback
		"""
		
		self._tickCount = 0
		self._startTick = self._pi.get_current_tick()
		self._cb = pi.callback(self._gpio, pigpio.FALLING_EDGE, self._cbf)
		while True:
			time.sleep(1.0)
			if self._tickCount > self._maxCount:
				break

	def terminate(self):

		self._cb.cancel()
		self._duration = pigpio.tickDiff(self._startTick, self._endTick)

	def activity(self):
		"""
		Compute activity and return
		"""
		return self._maxCount * 60.0 * 1000.0 / self._duration

	def _cbf(self, gpio, level, tick):

		if level == 0: # Falling edge.
			self._tickCount += 1 # increase tick count
			self._endTick = tick
			
		elif level == 2: # Watchdog timeout.
			pass

if __name__ == "__main__":

	COUNTER_GPIO = 17 	# which GPIO to use
	MAX_COUNT = 5 		# measure activity for 250 events

	# client = mqtt.Client()
	# client.on_connect = on_connect
	
	# client.connect("localhost", 1883, 60)
	# client.loop_start()

	pi = pigpio.pi()

	p = RadCounter(pi, COUNTER_GPIO, MAX_COUNT)

	while 1:
		# measure
		p.start()
		p.terminate()
		a = p.activity()
		
		print a
		
		# publish
		# client.publish("WS74/radioactivity", a)
		
	pi.stop()


