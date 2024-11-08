import pytest
import subprocess

@pytest.fixture(scope='session')
def mockallan_process():

	proc = subprocess.Popen(
		args=["mockallan"],
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
	)
	import time

	# time.sleep(0.25)

	proc.wait()

	# assert not proc.poll(), 
	# b = proc.stdout.read().decode("utf-8")

	yield proc

	proc.terminate()
