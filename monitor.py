#!/usr/bin/env python

# This script is designed to be executed from the command line
# with the following syntax:
# user.InterfaceMonitor.py '(device name)' (ON | OFF)
# Example:
# user.InterfaceMonitor.py 'Cisco Switch 1' OFF


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
        if (interface.operStatus == 1 and interface.adminStatus == 1):
                interface.monitor = True
                print interface.interfaceName + ' monitoring set to True'
        else:
                interface.monitor = False
                print interface.interfaceName + ' monitoring set to False'

commit()
