#!/usr/bin/python3

from MPU9250.MPU9250 import *
from hal import accelerometer
import numpy as np

class mpu9250(accelerometer):

    def __init__(self, args):
        self.calibration_a = np.diag(np.full(3, 1))
        self.calibration_b = np.full(3, 0)
        self.mpu = MPU9250()
        self.mpu.initialize()

    def measure_raw(self):
        data = self.mpu.get_accel()
        data = np.array([data["x"], data["y"], data["z"]])
        return data

    def measure(self):
        data = self.measure_raw()
        return np.matmul(data, self.calibration_a) + self.calibration_b

    def set_calibration(self, a, b):
        self.calibration_a = a
        self.calibration_b = b

    def info(self):
        return "accelerometer mpu9250 wrapper"

if __name__ == "__main__":
    acc = mpu9250({})
    print("acceleration data", acc.measure())

