#!/bin/sh

# Your Zenoss server settings.
# The URL to access your Zenoss5 Endpoint
ZENOSS_URL="https://192.168.0.203:8888"
ZENOSS_USERNAME="admin2"
ZENOSS_PASSWORD="Access123"

# Generic call to make Zenoss JSON API calls easier on the shell.
zenoss_api () {
    ROUTER_ENDPOINT=$1
    ROUTER_ACTION=$2
    ROUTER_METHOD=$3
    DATA=$4

    if [ -z "${DATA}" ]; then
        echo "Usage: zenoss_api <endpoint> <action> <method> <data>"
        return 1
    fi
# add a -k for the curl call to ignore the default cert
    curl \
        -k \
        -u "$ZENOSS_USERNAME:$ZENOSS_PASSWORD" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "{\"action\":\"$ROUTER_ACTION\",\"method\":\"$ROUTER_METHOD\",\"data\":[$DATA], \"tid\":1}" \
        "$ZENOSS_URL/zport/dmd/$ROUTER_ENDPOINT"
}


##############METHOD########33
zenoss_api device_router DeviceRouter setComponentsMonitored '{"uids":"/zport/dmd/Devices/Server/SSH/Linux/devices/192.168.1.32/os/interfaces/","monitor":"False","hashcheck":""}'
