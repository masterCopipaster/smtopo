#!/usr/bin/python3

import serial
from parse import parse
from hal import laser

class laser_basic(laser):

    def __init__(self, args):
        self.ser = serial.Serial(args["dev"], 19200, timeout = 1)

    def __del__(self):
        self.ser.close()

    def execute_command(self, cmd):
        #print(cmd)
        self.ser.write(cmd)
        return self.ser.readline()

    def on(self):
        return self.execute_command(b'O') == b'O,OK!\r\n'

    def off(self):
        return self.execute_command(b'C') == b'C,OK!\r\n'

    def measure(self):
        resp = self.execute_command(b'D').decode("ascii").strip()
        parsed = parse("D: {:f}m,{}", resp)
        try:
            dist = parsed[0]
            return True, dist
        except:
            return False, resp

    def info(self):
        return self.execute_command(b'S').decode("ascii")


if __name__ == "__main__":
    l = laser_basic({"dev":"/dev/ttyS0"})
    print("on operation:", l.on())
    print("dist:", l.measure())
    print("off operation", l.off())
    print("info:", l.info())
