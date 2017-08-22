#!/usr/bin/python

#This is a sample script todisable moitoring for ethernet interfaces that are 
#in a down/Down config. 

#Import whats needed
import json
import urllib
import urllib2
import ssl
import time
import logging
import pdb

#edit for logging
logging.basicConfig(filename='disablePorts.log',level=logging.DEBUG)

#Warning!! this is to ignore invalid certificates!! Its used on lines 30-31
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#set url, user/pass and device class here
ZENOSS_INSTANCE = 'https://zenoss5.zenoss-cc-master.prod.aws.glic.com'
ZENOSS_USERNAME = ''
ZENOSS_PASSWORD = ''
DeviceClass = "/zport/dmd/Devices/Network/Cisco/Nexus/"

#We really only need the Device router here
ROUTERS = { 'DeviceRouter': 'device',
            'PropertiesRouter': 'properties',
            'ServiceRouter' : 'service' }

class API():
    def __init__(self, debug=False):
        #Warning!! the following 2 lines ignore certs!
        self.urlOpener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx))
        self.urlOpener.add_handler(urllib2.HTTPCookieProcessor())
        #uncomment the following 2 lines for security!!
        #self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        #self.urlOpener.add_handler(urllib2.HTTPHandler(context=ctx))
        if debug:
            self.urlOpener.add_handler(urllib2.HTTPHandler(debuglevel=1))
        self.reqCount = 1

        loginParams = urllib.urlencode(dict(
            __ac_name=ZENOSS_USERNAME,
            __ac_password=ZENOSS_PASSWORD,
            submitted='true',
            came_from=ZENOSS_INSTANCE + '/zport/dmd'))
        self.urlOpener.open(
            ZENOSS_INSTANCE + '/zport/acl_users/cookieAuthHelper/login',
            loginParams)

    def _router_request(self, router, method, data=[]):
        if router not in ROUTERS:
            raise Exception('Router "' + router + '" not available.')

        # Contruct a standard URL request for API calls
        req = urllib2.Request(ZENOSS_INSTANCE + '/zport/dmd/' +
                              ROUTERS[router] + '_router')

        req.add_header('Content-type', 'application/json; charset=utf-8')

        # Convert the request parameters into JSON
        reqData = json.dumps([dict(
            action=router,
            method=method,
            data=data,
            type='rpc',
            tid=self.reqCount)])
        print "Payload generated as {}".format(str(reqData))

        self.reqCount += 1

        # Submit the request and convert the returned JSON to objects
        return json.loads(self.urlOpener.open(req, reqData).read())

if __name__ == '__main__':
    api = API(debug=False)
    #pdb.set_trace()

    #get uid's and format them for json
    dc1b = api._router_request('DeviceRouter', 'getDeviceUids',
                                       data=[{'uid': DeviceClass}])
    count = 1
    devTotal = len(dc1b["result"]["devices"])
    devList = []
    for device in dc1b["result"]["devices"]:
        devList.append(device)
    print devList[count - 1]
    print devTotal

    #get devices
    while count <= devTotal:
        currentDevice = devList[(count - 1)]
        #count = coun
        #get device components
        total = 1
        start = 0
        comps = {'result':{'data':[]}}
        while total != 0:
            result = api._router_request('DeviceRouter', 'getComponents',
                                 data=[{'uid': currentDevice, 'limit': 50, 'start': start, 'meta_type': 'CiscoEthernetInterface', 'keys': ("uuid", "meta_type", "id", "name", "uid", "combined_status", "monitor", "monitored")}]) #zproxy timeout, type
            comps["result"]["data"].extend(result['result']['data'])
            total = len(result["result"]["data"])
            start += total
       
        compCount = len(comps["result"]["data"])
        compIteration = 1
        count = count  + 1
        #component = compsJson["result"]["data"][compIteration]
        to_disable = []
        while compIteration <= compCount:
            component = comps["result"]["data"][compIteration - 1]
            compIteration = compIteration + 1
            logging.info("Component name: %s",  component["name"])
            logging.info("Component uid: %s",  component["uid"])
            logging.info("admin status: %s",  component["combined_status"]["admin"])
            logging.info("operational status: %s",  component["combined_status"]["oper"])
            logging.info("Component is monitored: %s",  component["monitored"])
            logging.info("Component is not manually disabled: %s",  component["monitor"])
            if 'Cisco/ASA' not in component["uid"]:
                if (component["combined_status"]["admin"] != True) and (component["combined_status"]["oper"] != True): #added by fg 
                    to_disable.append(component["uid"])
                    if len(to_disable) >= 50:
                        result = api._router_request('DeviceRouter', 'setComponentsMonitored', data=[{'uids':to_disable, 'monitor':False, 'hashcheck': ""}])
                        logging.info("result of unmonitor: %r", result)
                        to_disable = []
        if to_disable:
            result = api._router_request('DeviceRouter', 'setComponentsMonitored', data=[{'uids':to_disable, 'monitor':False, 'hashcheck': ""}])
            logging.info("result of unmonitor: %r", result)



