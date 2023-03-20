#!/usr/bin/python3
import smbus
import time
import os

STATUS_ADDR = 0
STATUS_OK = 5
STATUS_TX_FAIL = 1
STATUS_ON_TX = 2
STATUS_RX_NORESP = 3
STATUS_RX_NOFULL = 4
RX_POLL_PERIOD = 0.01
RX_POLL_TIMEOUT = 2

class i2cuart():
    def __init__(self, args={"bus":4, "addr":0x58}):
        self.bus = args["bus"]
        self.addr = args["addr"]
        self.i2c = smbus.SMBus(self.bus)

    def read_status(self):
        res = self.i2c.read_byte_data(self.addr, STATUS_ADDR)
        #print(res)
        return res

    def write(self, d):
        self.i2c.write_byte_data(self.addr, 0x0, ord(d))
        return True
        
    def read(self, timeout=RX_POLL_TIMEOUT, period=RX_POLL_PERIOD):
        starttime = time.time()
        while time.time() - starttime < timeout and self.read_status() != STATUS_OK:
            time.sleep(period)
        res = []
        for i in range(1, 0xf):
            res.append(self.i2c.read_byte_data(self.addr, i))
        return bytes(res).decode("ascii")


if __name__ == "__main__":
    adapter = i2cuart()
    adapter.write("O")
    time.sleep(1)
    adapter.write("D")
    print(adapter.read())
    time.sleep(1)
    adapter.write("C")