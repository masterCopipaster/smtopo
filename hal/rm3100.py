#!/usr/bin/python3

import subprocess
from hal import magnetometer
import numpy as np
import json

readerbin = "/usr/local/src/rm3100-runMag-master/runMag"

class rm3100(magnetometer):

    def __init__(self, args):
        self.calibration_a = np.diag(np.full(3, 1))
        self.calibration_b = np.full(3, 0)
        self.bus = args["bus"]
        self.addr = args["addr"]
        if "count" in args:
            self.count = args["count"]
        else:
            self.count = 100

    def measure_raw(self):
        cmd = [readerbin, f"-M {self.addr}", f"-b {self.bus}" ,f"-c {self.count}", "-s", "-m", "-j"]
        #print("starting rm3100 subprocess")
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        #print(result)
        ddict = json.loads(result.stdout.decode("utf-8"))
        #print(ddict)
        data = np.array([float(ddict["x"]), float(ddict["y"]), float(ddict["z"])])
        return data

    def measure(self):
        data = self.measure_raw()
        return np.matmul(data, self.calibration_a) + self.calibration_b 
    
    def set_calibration(self, a, b):
        self.calibration_a = a
        self.calibration_b = b
    def info(self):
        return "runMag utility based rm3100 wrapper"
        
if __name__ == "__main__":
    l = rm3100({"bus":3, "addr":22})
    print("magnetic data:", l.measure_raw())
    print("info:", l.info())
