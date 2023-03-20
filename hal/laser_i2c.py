#!/usr/bin/python3

import serial
from parse import parse
from hal import laser
import i2cuart

class laser_i2c(laser):

    def __init__(self, args={"bus":4, "addr":0x58}):
        self.adapter = i2cuart.i2cuart(args={"bus":args["bus"], "addr":args["addr"]})

    def execute_command(self, cmd):
        #print(cmd)
        self.adapter.write(cmd)
        return self.adapter.read()

    def on(self):
        return self.adapter.write('O')

    def off(self):
        return self.adapter.write('C')

    def measure(self):
        resp = self.execute_command('D').strip()
        #print(resp)
        parsed = parse("D: {:f}{}", resp)
        try:
            dist = parsed[0]
            return True, dist
        except:
            return False, resp

    def info(self):
        return self.execute_command('S')


if __name__ == "__main__":
    l = laser_i2c()
    print("on operation:", l.on())
    print("dist:", l.measure())
    print("off operation", l.off())
    print("info:", l.info())
