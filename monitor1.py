#!/usr/bin/env python

# This script is designed to be executed from the command line
# with the following syntax:
# user.InterfaceMonitor.py '(device name)' (ON | OFF)
# Example:
# user.InterfaceMonitor.py 'Cisco Switch 1' OFF
a=input("Enter Oper status value UP(1) or DOWN(2):\n")
b=input("Enter admin status value UP(1) or DOWN(2):\n")
c=input("Enter Monitor status True or False(Format : True or False)\n")

import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit
import sys

dmd = ZenScriptBase(connect=True).dmd
deviceName = sys.argv[1]
device = dmd.Devices.findDevice(deviceName)
if device is None:
   print '\nDevice not found in dmd.\n'
   sys.exit()

for interface in device.os.interfaces():
    if interface.isLockedFromUpdates():
        print interface.interfaceName + ' is locked from updates, skipping'
    else:
        if (interface.operStatus == a and interface.adminStatus == b):
                interface.monitor = c
                print interface.interfaceName + ' monitoring set to '+ str(c)


commit()
