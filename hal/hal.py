import numpy as np

#laser disto abstract class
class laser:

    def __init__(self):
        pass

    def on(self):
        print("laser ON")

    def off(self):
        print("laser OFF")

    def measure(self):
        return 1.0

class magnetometer:

    def __init__(self):
        self.calibration_a = np.diag(np.full(3, 1))
        self.calibration_b = np.full(3, 0)

    def measure_raw(self):
        data = np.array(1.0, 0.0, 0.0)
        return data

    def measure(self):
        data = np.array(1.0, 0.0, 0.0)
        return np.matmul(data, self.calibration_a) + self.calibration_b 
    
    def calibrate(self, a, b):
        self.calibration_a = a
        self.calibration_b = b