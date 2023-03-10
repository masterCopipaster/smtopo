import numpy as np

#laser disto abstract class
class laser:

    def __init__(self, args):
        self.data = args["data"]

    def on(self):
        print("laser ON")

    def off(self):
        print("laser OFF")

    def measure(self):
        return self.data

    def info(self):
        return "laser module abstract stub"

class magnetometer:

    def __init__(self, args):
        self.calibration_a = np.diag(np.full(3, 1))
        self.calibration_b = np.full(3, 0)
        self.data = np.array(args["data"])

    def measure_raw(self):
        return self.data

    def measure(self):
        data = self.measure_raw()
        return np.matmul(data, self.calibration_a) + self.calibration_b 
    
    def set_calibration(self, a, b):
        self.calibration_a = a
        self.calibration_b = b

    def info(self):
        return "magnetometer module abstract stub"

class accelerometer:

    def __init__(self, args):
        self.calibration_a = np.diag(np.full(3, 1))
        self.calibration_b = np.full(3, 0)
        self.data = np.array(args["data"])

    def measure_raw(self):
        return self.data

    def measure(self):
        data = self.measure_raw()
        return np.matmul(data, self.calibration_a) + self.calibration_b 
    
    def set_calibration(self, a, b):
        self.calibration_a = a
        self.calibration_b = b

    def info(self):
        return "accelerometer module abstract stub"
