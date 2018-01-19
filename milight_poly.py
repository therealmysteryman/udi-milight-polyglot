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
        self.port = ""
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
                self.port = "5987"

            if self.host == "" or self.port == "" :
                LOGGER.error('MiLight requires \'host\' parameters to be specified in custom configuration.')
                return False
            else:
                self.discover()
        except Exception as ex:
            LOGGER.error('Error starting MiLight NodeServer: %s', str(ex))

    def shortPoll(self):
        pass

    def longPoll(self):
        pass

    def query(self):
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        time.sleep(1)
        self.addNode(MiLightGroup(self, self.address, 'bridge', 'Bridge'))
        self.addNode(MiLightGroup(self, self.address, 'zone1', 'Zone1'))
        self.addNode(MiLightGroup(self, self.address, 'zone2', 'Zone2'))
        self.addNode(MiLightGroup(self, self.address, 'zone3', 'Zone3'))
        self.addNode(MiLightGroup(self, self.address, 'zone4', 'Zone4'))

    def delete(self):
        LOGGER.info('Deleting MiLight')
        
    id = 'controller'
    commands = {'DISCOVER': discover}
    drivers = [{'driver': 'ST', 'value': 0, 'uom': 2}]
    
class MiLightGroup(polyinterface.Node):
    """
    This is the class that all the Nodes will be represented by. You will add this to
    Polyglot/ISY with the controller.addNode method.

    Class Variables:
    self.primary: String address of the Controller node.
    self.parent: Easy access to the Controller Class from the node itself.
    self.address: String address of this Node 14 character limit. (ISY limitation)
    self.added: Boolean Confirmed added to ISY

    Class Methods:
    start(): This method is called once polyglot confirms the node is added to ISY.
    setDriver('ST', 1, report = True, force = False):
        This sets the driver 'ST' to 1. If report is False we do not report it to
        Polyglot/ISY. If force is True, we send a report even if the value hasn't changed.
    reportDrivers(): Forces a full update of all drivers to Polyglot/ISY.
    query(): Called when ISY sends a query request to Polyglot for this specific node
    """
    def __init__(self, controller, primary, address, name):
        """
        Optional.
        Super runs all the parent class necessities. You do NOT have
        to override the __init__ method, but if you do, you MUST call super.

        :param controller: Reference to the Controller class
        :param primary: Controller address
        :param address: This nodes address
        :param name: This nodes name
        """
        super(MiLightGroup, self).__init__(controller, primary, address, name)
        self.host = self.parent.host
        self.port = self.parent.port
        self.timeout = 5.0
        
        # Light Group 1-4 0=ALL
        if name == 'Zone1':
            self.grpNum = 1
        elif name == 'Zone2':
            self.grpNum = 2
        elif name == 'Zone3':
            self.grpNum = 3
        elif name == 'Zone4':
            self.grpNum = 4
        elif name == 'bridge':
            self.grpNum = 5         
        else:
            self.grpNum = 0
            
    def start(self):
        self.setDriver('ST', 1)
        pass

    def setOn(self, command):
        milight.setup(ip=self.host, port=self.port, timeout_sec=self.timeout):
        if self.grpNum == 5:
            milight.turnOnWifiBridgeLamp()
        else:
            milight.turnOn(zoneId=self.grpNum)
        milight.close()
        self.setDriver('ST', 1)

    def setOff(self, command):
        milight.setup(ip=self.host, port=self.port, timeout_sec=self.timeout):
        if self.grpNum == 5:
            milight.turnOffWifiBridgeLamp()
        else:
            milight.turnOff(zoneId=self.grpNum)
        milight.close()
        self.setDriver('ST', 0)

    def query(self):
        """
        Called by ISY to report all drivers for this node. This is done in
        the parent class, so you don't need to override this method unless
        there is a need.
        """
        self.reportDrivers()


    drivers = [{'driver': 'ST', 'value': 0, 'uom': 2}]
    """
    Optional.
    This is an array of dictionary items containing the variable names(drivers)
    values and uoms(units of measure) from ISY. This is how ISY knows what kind
    of variable to display. Check the UOM's in the WSDK for a complete list.
    UOM 2 is boolean so the ISY will display 'True/False'
    """
    id = 'MILIGHT_GROUP'
    """
    id of the node from the nodedefs.xml that is in the profile.zip. This tells
    the ISY what fields and commands this node has.
    """
    commands = {
                    'DON': setOn, 'DOF': setOff
                }
    """
    This is a dictionary of commands. If ISY sends a command to the NodeServer,
    this tells it which method to call. DON calls setOn, etc.
    """

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('MiLightNodeServer')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
