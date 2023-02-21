#!/usr/bin/python3
import numpy as np
from threading import Thread
from threading import Event
class orientation:
    def __init__(self, config):
        mag_module = config["magnetometer"]["module"]
        mag_class = config["magnetometer"]["class"]
        mag_args = config["magnetometer"]["args"]
        exec(f"import {mag_module}\nself.mag = {mag_module}.{mag_class}(mag_args)")

        acc_module = config["accelerometer"]["module"]
        acc_class = config["accelerometer"]["class"]
        acc_args = config["accelerometer"]["args"]
        exec(f"import {acc_module}\nself.acc = {acc_module}.{acc_class}(acc_args)")
        print("magnetometer attached:", self.mag.info())
        print("accelerometer attached:", self.acc.info())

    def get_acc_data(self):
        self.acc_vect = self.acc.measure()
        return self.acc_vect

    def get_mag_data(self):
        self.mag_vect = self.mag.measure()
        return self.mag_vect

    def get_data(self):
        self.mag_vect = self.mag.measure()
        self.acc_vect = self.acc.measure()
        return self.mag_vect, self.acc_vect

    def acc_data_async_worker(self, stopevent):
        acc_acc = np.array([0.0, 0.0, 0.0])
        num = 0
        while True:
            acc_acc += self.acc.measure()
            num += 1
            #print("acc measured")
            if stopevent.is_set():
                #print("stop event")
                break
        print(f"async worker exiting n = {num}")
        self.acc_vect = acc_acc / num

    def get_data_async_by_acc(self):
        stopevent = Event()
        acc_thread = Thread(target = orientation.acc_data_async_worker, args = (self,stopevent,))
        acc_thread.start()
        #print("measuring mag")
        self.mag_vect = self.mag.measure()
        #print("mag measured")
        stopevent.set()
        acc_thread.join()
        return self.mag_vect, self.acc_vect

    def incl(self):
        return np.degrees(np.arccos(self.acc_vect[0]/np.linalg.norm(self.acc_vect))) - 90

    def azimuth(self):
        mgplane = np.cross(self.acc_vect, self.mag_vect)
        #print(mgplane)
        xgplane = np.cross(self.acc_vect, np.array([1, 0, 0]))
        #print(xgplane)
        angle = np.degrees(np.arccos(np.dot(mgplane/np.linalg.norm(mgplane), xgplane/np.linalg.norm(xgplane))))
        angledir = np.dot(np.cross(mgplane, xgplane), self.acc_vect) > 0
        if angledir:
            angle = 360 - angle
        return angle

if __name__ == "__main__":
    import sys
    import json
    config = json.loads(open(sys.argv[1]).read())
    pos = orientation(config)
    print("data", pos.get_data_async_by_acc())
    print("inclination", pos.incl())
    print("azimuth", pos.azimuth())

