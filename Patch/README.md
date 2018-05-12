/etc/dnsmasq.d
mv 05-restrict.conf /etc/dnsmasq.d/
05-restrict.conf

/opt/pihole
patch gravity.sh < gravity.sh.diff
gravity.sh.diff

/etc/hosts
cat hosts >> /etc/hosts
hosts