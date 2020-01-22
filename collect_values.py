#!/usr/bin/env python3
import logging
import sys
import locale
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
    
    locale.setlocale(locale.LC_ALL, '')
    
    if not home.get_current_state():
        print("home.get_current_state()={}".format(home.get_current_state()))
        return

    sortedGroups = sorted(home.groups, key=attrgetter("groupType", "label"))
    for g in sortedGroups:
        print(type(g).__name__ +" "+g.label+":")
        if (isinstance(g, HeatingGroup)):
            # first print Sensor
            sensorDevices = []
            heatingThermostats= [];
            for d in g.devices:
                if isinstance(d, TemperatureHumiditySensorWithoutDisplay):
                    # https://homematicip-rest-api.readthedocs.io/en/latest/homematicip.html#homematicip.device.TemperatureHumiditySensorWithoutDisplay
                    sensorDevices.append(d)
                elif isinstance(d, HeatingThermostat):
                    heatingThermostats.append(d)
            
            if (len(heatingThermostats)>0):        
                f = open(g.label + ".csv", "a+")
                for d in sorted(sensorDevices):
                    print("  humidity {} {} {}".format(d.label, locale.str(d.actualTemperature), locale.str(d.humidity)))
                    f.write("{}\t{}\t{}".format(datetime.now(), locale.str(d.actualTemperature), locale.str(d.humidity)))
                # Then all HeatingThermostat
                for d in sorted(heatingThermostats):
                    print("  valvePosition {} {} {}".format(d.label, locale.str(d.valveActualTemperature), locale.str(d.valvePosition*100)))
                    f.write("\t{}\t{}".format(locale.str(d.valveActualTemperature), locale.str(d.valvePosition*100)))
                f.write("\n")
                f.close()


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
