#!/bin/bash
# dnsmasq file for safesearch
wget -O /etc/dnsmasq.d/05-restrict.conf https://raw.githubusercontent.com/mchangrh/Shutter/master/Patch/05-restrict.conf
# patch gravity.sh
curl https://raw.githubusercontent.com/mchangrh/Shutter/master/Patch/gravity.diff | patch /opt/pihole/gravity.sh
# Add to hosts file
curl https://raw.githubusercontent.com/mchangrh/Shutter/master/Patch/hosts >> /etc/hosts
