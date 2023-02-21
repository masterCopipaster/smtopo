#!/usr/bin/python3

from flask import Flask
import orientation
import json
import argparse
import threading

parser = argparse.ArgumentParser(description="hardware management server")

parser.add_argument("--conf", dest = "conf", default = "hal/default_conf.json", help = "configuration json file")

args = parser.parse_args()

config = json.loads(open(args.conf).read())

pos = orientation.orientation(config)

laser_module = config["laser"]["module"]
laser_class = config["laser"]["class"]
laser_args = config["laser"]["args"]
exec(f"import {laser_module}\nlaser = {laser_module}.{laser_class}(laser_args)")
print("laser attached:", laser.info())


app = Flask("hardware server")

@app.route('/orientation/', methods=['GET'])
def get_orientation():
    pos.get_data_async_by_acc()
    return json.dumps({"incl":pos.incl(), "azimuth":pos.azimuth()})

def async_orient_measure_worker():
    pos.get_data_async_by_acc()

@app.route('/shot/', methods=['GET'])
def get_shot():
    thread = threading.Thread(target = pos.get_data_async_by_acc)
    thread.start()
    distance = laser.measure()
    thread.join()
    return json.dumps({"incl":pos.incl(), "azimuth":pos.azimuth(), "distance":distance})

if __name__ == '__main__':
    app.run(port='8000')
