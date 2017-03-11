import sys
from subprocess import Popen, PIPE

class Outputs:
    def __init__(self, on_arcade):
        self.state = [False, False]

        if on_arcade:
            self.process = Popen('./keypress_emu.py', stdin=PIPE)
            self.fd = self.process.stdin

        else:
            self.process = None
            self.fd = sys.stdout

    def write(self):
        value = 0

        for i in range(len(self.state)):
            value |= int(self.state[i]) << i

        self.fd.write(str(value) + "\n")

    def stop(self):
        if self.process:
            print 'killed it'
            self.process.kill()
