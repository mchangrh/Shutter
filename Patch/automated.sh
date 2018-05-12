#!/bin/bash

# Links
DNSMASQ="https://raw.githubusercontent.com/mchangrh/Shutter/master/Patch/05-restrict.conf"
GRAVITY="https://raw.githubusercontent.com/mchangrh/Shutter/master/Patch/gravity.diff"
HOSTS="https://raw.githubusercontent.com/mchangrh/Shutter/master/Patch/hosts"


# dnsmasq file for safesearch
wget -O /etc/dnsmasq.d/05-restrict.conf $DNSMASQ

# patch gravity.sh
curl $GRAVITY | patch /opt/pihole/gravity.sh

# Add to hosts file
curl $HOSTS >> /etc/hosts
