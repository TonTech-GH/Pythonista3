import signal
import time

def task(arg1, arg2):
	print(time.time())

print(time.time())
signal.signal(signal.SIGALRM, task)
signal.setitimer(signal.ITIMER_REAL, 2.0, 1.0)

while True:
	pass

