#!/usr/bin/env python3

"""
This is a NodeServer for MiLight Protocol V6 written by automationgeek (Jean-Francois Tremblay) 
based on the NodeServer template for Polyglot v2 written in Python2/3 by Einstein.42 (James Milne) milne.james@gmail.com
MiLight functionality based on 'Milight-Wifi-Bridge-3.0-Python-Library' project by QuentinCG (https://github.com/QuentinCG/Milight-Wifi-Bridge-3.0-Python-Library)
"""

import polyinterface
import time
import json
import sys
from MilightWifiBridge import MilightWifiBridge

LOGGER = polyinterface.LOGGER
SERVERDATA = json.load(open('server.json'))
VERSION = SERVERDATA['credits'][0]['version']

class Controller(polyinterface.Controller):

    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'MiLight'
        self.initialized = False
        self.milight_host = ""
        self.milight_port = 5987
        self.tries = 0

    def start(self):
        LOGGER.info('Started MiLight for v2 NodeServer version %s', str(VERSION))
        self.setDriver('ST', 0)
        try:
            if 'host' in self.polyConfig['customParams']:
                self.milight_host = self.polyConfig['customParams']['host']
            else:
                self.milight_host = ""

            if 'port' in self.polyConfig['customParams']:
                self.milight_port = self.polyConfig['customParams']['port']
            else:
                self.milight_port = 5987

            if self.milight_host == "" :
                LOGGER.error('MiLight requires \'host\' parameters to be specified in custom configuration.')
                return False
            else:
                self.setDriver('ST', 1)
                self.discover()
                self.reportDrivers()
        except Exception as ex:
            LOGGER.error('Error starting MiLight NodeServer: %s', str(ex))

    def shortPoll(self):
        pass

    def longPoll(self):
        pass

    def query(self):
        self.reportDrivers()
        
    def discover(self, *args, **kwargs):
        time.sleep(1)
        self.addNode(MiLightBridge(self, self.address, 'bridge', 'Bridge'))
        self.addNode(MiLightLight(self, self.address, 'zone1', 'Zone1'))
        self.addNode(MiLightLight(self, self.address, 'zone2', 'Zone2'))
        self.addNode(MiLightLight(self, self.address, 'zone3', 'Zone3'))
        self.addNode(MiLightLight(self, self.address, 'zone4', 'Zone4'))
        
    def delete(self):
        LOGGER.info('Deleting MiLight')
        
    id = 'controller'
    commands = {}
    drivers = [{'driver': 'ST', 'value': 0, 'uom': 2}]
    
class MiLightLight(polyinterface.Node):

    def __init__(self, controller, primary, address, name):

        super(MiLightLight, self).__init__(controller, primary, address, name)
        self.milight_timeout = 5.0
        self.milight_host = self.parent.milight_host
        self.milight_port = self.parent.milight_port
        
        self.myMilight = MilightWifiBridge()
        self.myMilight.setup(self.milight_host,self.milight_port,self.milight_timeout)
        
        # Set Zone
        if name == 'Zone1':
            self.grpNum = 1
        elif name == 'Zone2':
            self.grpNum = 2
        elif name == 'Zone3':
            self.grpNum = 3
        elif name == 'Zone4':
            self.grpNum = 4
            
    def start(self):
        # Initial Value
        self.setDriver('ST', 0)
        self.setDriver('GV1', 0)
        self.setDriver('GV2', 0)
        self.setDriver('GV3', 100)
        self.setDriver('GV4', 1)
        self.setDriver('GV5', 0) 
        self.reportDrivers()
        
    def setOn(self, command):
        self.__MilightConnect()
        self.myMilight.turnOn(zoneId=self.grpNum)
        self.__MilightDisconnect()
        self.setDriver('ST', 100)

    def setOff(self, command):
        self.__MilightConnect()
        self.myMilight.turnOff(zoneId=self.grpNum)
        self.__MilightDisconnect()
        self.setDriver('ST', 0)
        
    def setColor(self, command):
        intColor = int(command.get('value'))
        self.myMilight.setColor(intColor,self.grpNum) 
        self.setDriver('GV1', intColor,True)
        
    def setSaturation(self, command):
        intSat = int(command.get('value'))
        self.myMilight.setSaturation(intSat,self.grpNum) 
        self.setDriver('GV2', intSat,True)
        
    def setBrightness(self, command):
        intBri = int(command.get('value'))
        self.myMilight.setBrightness(intBri,self.grpNum) 
        self.setDriver('GV3', intBri,True)

    def setTempColor(self, command):
        intTemp = int(command.get('value'))
        self.myMilight.setTemperature(intTemp,self.grpNum) 
        self.setDriver('GV5', intTemp,True)
        
    def setEffect(self, command):
        intEffect = int(command.get('value'))
        self.myMilight.setDiscoMode(intEffect,self.grpNum)
        self.setDriver('GV4', intEffect,True)
        
    def setWhiteMode(self, command):
        self.myMilight.setWhiteMode(self.grpNum)
        
    def setNightMode(self, command):
        self.myMilight.setNightMode(self.grpNum)
        
    def query(self):
        self.reportDrivers()
             
    drivers = [{'driver': 'ST', 'value': 0, 'uom': 78},
               {'driver': 'GV1', 'value': 0, 'uom': 100},
               {'driver': 'GV2', 'value': 0, 'uom': 51},
               {'driver': 'GV3', 'value': 0, 'uom': 51},
               {'driver': 'GV5', 'value': 0, 'uom': 51},
               {'driver': 'GV4', 'value': 1, 'uom': 100}]
    id = 'MILIGHT_LIGHT'
    commands = {
                    'DON': setOn,
                    'DOF': setOff,
                    "SET_COLOR": setColor,
                    "SET_SAT": setSaturation,
                    "SET_BRI": setBrightness,
                    "CLITEMP": setTempColor,
                    "SET_EFFECT": setEffect,
                    "WHITE_MODE": setWhiteMode,
                    "NIGHT_MODE": setNightMode
                }
    
class MiLightBridge(polyinterface.Node):

    def __init__(self, controller, primary, address, name):

        super(MiLightBridge, self).__init__(controller, primary, address, name)
        self.milight_timeout = 5.0
        self.milight_host = self.parent.milight_host
        self.milight_port = self.parent.milight_port
        
        self.myMilight = MilightWifiBridge()
        self.myMilight.setup(self.milight_host,self.milight_port,self.milight_timeout)
             
    def start(self):
        # Init Value
        self.setDriver('ST', 0)
        self.setDriver('GV1', 0)
        self.setDriver('GV3', 100)
        self.setDriver('GV4', 1)
        self.reportDrivers()

    def setOn(self, command):
        self.myMilight.turnOnWifiBridgeLamp()
        self.setDriver('ST', 100, True)

    def setOff(self, command):
        self.myMilight.turnOffWifiBridgeLamp()
        self.setDriver('ST', 0, True)
        
    def setColor(self, command):
        intColor = int(command.get('value'))
        self.myMilight.setColorBridgeLamp(intColor) 
        self.setDriver('GV1', intColor,True)
        
    def setBrightness(self, command):
        intBri = int(command.get('value'))
        self.myMilight.setBrightnessBridgeLamp(intBri) 
        self.setDriver('GV3', intBri,True)
        
    def setEffect(self, command):
        intEffect = int(command.get('value'))
        self.myMilight.setDiscoModeBridgeLamp(intEffect)
        self.setDriver('GV4', intEffect,True)
        
    def setWhiteMode(self, command):
        self.myMilight.setWhiteModeBridgeLamp()
  
    def query(self):
        self.reportDrivers()
        
    drivers = [{'driver': 'ST', 'value': 0, 'uom': 78},
               {'driver': 'GV1', 'value': 0, 'uom': 100},
               {'driver': 'GV3', 'value': 0, 'uom': 51},
               {'driver': 'GV4', 'value': 1, 'uom': 100}]
    id = 'MILIGHT_BRIDGE'
    commands = {
                    'DON': setOn,
                    'DOF': setOff,
                    "SET_COLOR": setColor,
                    "SET_BRI": setBrightness,
                    "SET_EFFECT": setEffect,
                    "WHITE_MODE": setWhiteMode
                }
    
if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('MiLightNodeServer')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
