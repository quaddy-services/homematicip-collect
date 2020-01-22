#!/usr/bin/env python3
import logging
import sys
import time
from datetime import datetime
from argparse import ArgumentParser
from collections import namedtuple
from logging.handlers import TimedRotatingFileHandler

import homematicip
from homematicip.device import *
from homematicip.group import *
from homematicip.rule import *
from homematicip.home import Home
from homematicip.base.helpers import handle_config


logger = None


def create_logger(level, file_name):
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = (
        TimedRotatingFileHandler(file_name, when="midnight", backupCount=5)
        if file_name
        else logging.StreamHandler()
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    return logger


server_config = None


def fake_download_configuration():
    global server_config
    if server_config:
        with open(server_config) as file:
            return json.load(file, encoding="UTF-8")
    return None


def main():

	_config = homematicip.find_and_load_config_file()
	if _config is None:
		print("Could not find configuration file. Script will exit")
		return

	global logger
	logger = create_logger(
		_config.log_level, _config.log_file
	)

	home = Home()
	home.set_auth_token(_config.auth_token)
	home.init(_config.access_point)

	if not home.get_current_state():
		print("home.get_current_state()={}".format(home.get_current_state()))
		return

	sortedDevices = sorted(home.devices, key=attrgetter("deviceType", "label"))
	# print("sortedDevices={}".format(sortedDevices))
	for d in sortedDevices:
		if isinstance(d, TemperatureHumiditySensorWithoutDisplay):
		  print("humidity {},{},{}".format(d.label,d.actualTemperature,d.humidity))
		  f=open(d.label+".csv", "a+")
		  f.write("{},{},{}\r\n".format(datetime.now(),d.actualTemperature,d.humidity))
		  f.close()
		elif isinstance(d, HeatingThermostat):
 			print("valvePosition {},{},{}".format(d.label,d.valveActualTemperature,d.valvePosition))
 			f=open(d.label+".csv", "a+")
 			f.write("{},{},{}\r\n".format(datetime.now(),d.valveActualTemperature,d.valvePosition))
 			f.close()
		else:
			print("{} {}".format(d.id, str(d)))



def printEvents(eventList):
    for event in eventList:
        print("EventType: {} Data: {}".format(event["eventType"], event["data"]))


def getRssiBarString(rssiValue):
    # Observed values: -93..-47
    width = 10
    dots = 0
    if rssiValue:
        dots = int(round((100 + rssiValue) / 5))
        dots = max(0, min(width, dots))

    return "[{}{}]".format("*" * dots, "_" * (width - dots))


if __name__ == "__main__":
    main()
