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
        self.host = ""
        self.port = 5987
        self.tries = 0

    def start(self):
        LOGGER.info('Started MiLight for v2 NodeServer version %s', str(VERSION))
        try:
            if 'host' in self.polyConfig['customParams']:
                self.host = self.polyConfig['customParams']['host']
            else:
                self.host = ""

            if 'port' in self.polyConfig['customParams']:
                self.port = self.polyConfig['customParams']['port']
            else:
                self.port = 5987

            if self.host == "" or self.port == "" :
                LOGGER.error('MiLight requires \'host\' parameters to be specified in custom configuration.')
                self.setDriver('ST', 0)
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
        self.reportDrivers()

    def query(self):
        for node in self.nodes:
            self.nodes[node].reportDrivers()
        
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
        self.host = self.parent.host
        self.port = self.parent.port
        self.myMilight = None
        self.timeout = 5.0
        
        # Set Zone
        if name == 'Zone1':
            self.grpNum = 1
        elif name == 'Zone2':
            self.grpNum = 2
        elif name == 'Zone3':
            self.grpNum = 3
        elif name == 'Zone4':
            self.grpNum = 4
         
        # Initial Value
        self.setDriver('ST', 0)
        self.setDriver('GV1', 0)
        self.setDriver('GV2', 0)
        self.setDriver('GV3', 100)
        self.setDriver('GV4', 1)
        self.setDriver('GV5', 0)
            
    def start(self):
        pass 

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
        
        self.__MilightConnect()
        self.myMilight.setColor(color=intColor, zoneId=self.grpNum) 
        self.__MilightDisconnect()
        self.setDriver('GV1', intColor)
        
    def setSaturation(self, command):
        intSat = int(command.get('value'))
        
        self.__MilightConnect()
        self.myMilight.setSaturation(saturation=intSat, zoneId=self.grpNum) 
        self.__MilightDisconnect()
        self.setDriver('GV2', intSat)
        
    def setBrightness(self, command):
        intBri = int(command.get('value'))
        
        self.__MilightConnect()
        self.myMilight.setBrightness(brightness=intBri, zoneId=self.grpNum) 
        self.__MilightDisconnect()
        self.setDriver('GV3', intBri)

    def setTempColor(self, command):
        intTemp = int(command.get('value'))
        
        self.__MilightConnect()
        self.myMilight.setTemperature(temperature=intTemp, zoneId=self.grpNum) 
        self.__MilightDisconnect()
        self.setDriver('GV5', intTemp)
        
    def setEffect(self, command):
        intEffect = int(command.get('value'))
        
        self.__MilightConnect()
        self.myMilight.setDiscoMode(discoMode=intEffect, zoneId=self.grpNum)
        self.__MilightDisconnect()
        self.setDriver('GV4', intEffect)
        
    def setWhiteMode(self, command):
        self.__MilightConnect()
        self.myMilight.setWhiteMode(zoneId=self.grpNum)
        self.__MilightDisconnect()
        
    def setNightMode(self, command):
        self.__MilightConnect()
        self.myMilight.setNightMode(zoneId=self.grpNum)
        self.__MilightDisconnect()
        
    def query(self):
        pass
     
    def __MilightConnect(self):
        try:
            self.myMilight = MilightWifiBridge()
            self.myMilight.setup(ip=self.host, port=self.port, timeout_sec=self.timeout)
        except Exception as ex:
            LOGGER.error('Error connecting to MiLight: %s', str(ex))

    def __MilightDisconnect(self):
        self.myMilight.close()
        self.myMilight = None
        
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
        self.host = self.parent.host
        self.port = self.parent.port
        self.myMilight = None
        self.timeout = 5.0
        
        # Init Value
        self.setDriver('ST', 0)
        self.setDriver('GV1', 0)
        self.setDriver('GV3', 100)
        self.setDriver('GV4', 1)
            
    def start(self):
        pass

    def setOn(self, command):
        self.__MilightConnect()
        self.myMilight.turnOnWifiBridgeLamp()
        self.__MilightDisconnect()
        #self.setDriver('ST', 100)

    def setOff(self, command):
        self.__MilightConnect()
        self.myMilight.turnOffWifiBridgeLamp()
        self.__MilightDisconnect()
        #self.setDriver('ST', 0)
        
    def setColor(self, command):
        intColor = int(command.get('value'))
        
        self.__MilightConnect()
        self.myMilight.setColorBridgeLamp(color=intColor) 
        self.__MilightDisconnect()
        self.setDriver('GV1', intColor)
        
    def setBrightness(self, command):
        intBri = int(command.get('value'))
        
        self.__MilightConnect()
        self.myMilight.setBrightnessBridgeLamp(brightness=intBri) 
        self.__MilightDisconnect()
        self.setDriver('GV3', intBri)
        
    def setEffect(self, command):
        intEffect = int(command.get('value'))
        
        self.__MilightConnect()
        self.myMilight.setDiscoModeBridgeLamp(discoMode=intEffect)
        self.__MilightDisconnect()
        self.setDriver('GV4', intEffect)
        
    def setWhiteMode(self, command):
        self.__MilightConnect()
        self.myMilight.setWhiteModeBridgeLamp()
        self.__MilightDisconnect()
  
    def query(self):
        pass
    
    def __MilightConnect(self):
        try:
            self.myMilight = MilightWifiBridge()
            self.myMilight.setup(ip=self.host, port=self.port, timeout_sec=self.timeout)
        except Exception as ex:
            LOGGER.error('Error connecting to MiLight Hub: %s', str(ex))

    def __MilightDisconnect(self):
        self.myMilight.close()
        self.myMilight = None
    
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
