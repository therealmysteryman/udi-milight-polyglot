## This nodeserver has been converted to run on PG3. The code has been moved to https://github.com/therealmysteryman/udi-milight-pg3.git



# MiLight V6 Polyglot V2 Node Server

![Build Status](https://travis-ci.org/therealmysteryman/udi-milight-polyglot.svg?branch=master)

This Poly provides an interface between Milight iBox 1 or 2 and Polyglot v2 server. Has been testing with RBGW Strip and MR16 bulb and  designed to work with the V6 protocol only. http://www.limitlessled.com/dev/

## Installation

Installation instructions

You can install from Polyglot V2 store or manually :

1. cd ~/.polyglot/nodeservers
2. git clone https://github.com/therealmysteryman/udi-milight-polyglot.git
3. run ./install.sh to install the required dependency.
4. Add a custom variable named host containing the IP Address of the Milight iBox ( eg : host 172.16.1.40 )
    You can add more then one iBox by seperating ip by comma (172.16.1.40,172.16.1.41).
.
## Source

1. Using this Python Library to control the Milight - https://github.com/QuentinCG/Milight-Wifi-Bridge-3.0-Python-Library
2. Based on the Node Server Template - https://github.com/Einstein42/udi-poly-template-python

## Release Notes

  - 2.4.1 08/11/2019
    - Updated MiLight Library
    - Bug Fixes
  - 2.3.7 05/11/2019
    - Added support to Polisy
  - 2.3.6 01/11/2018
    - Also send heartbeat on startup
  - 2.3.4 28/11/2018
    - Add heartbeat
    - Add auto update profile based on profile/version.txt
    - query reports drivers so ISY reboot gets the current status
