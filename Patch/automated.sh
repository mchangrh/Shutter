#!/bin/bash

# dnsmasq file for safesearch
wget -O /etc/dnsmasq.d/05-restrict.conf https://raw.githubusercontent.com/mchangrh/Shutter/master/PiHole%20Patches/05-restrict.conf

# patch gravity.sh
curl https://raw.githubusercontent.com/mchangrh/Shutter/master/PiHole%20Patches/gravity.sh.diff | patch /opt/pihole/gravity.sh

