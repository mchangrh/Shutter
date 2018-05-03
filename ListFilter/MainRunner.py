import ListPrepper

# Download and extract files
ListPrepper.extract()

# Delete all IP addresses
# 0.00035357900014787447
ListPrepper.strip_all_ip('domains', 'ippurge')

# Strip all domains matching site list
# 0.0007489019994864066
ListPrepper.domain_stripper('ippurge', 'domainpurge')

# add www version if it applies
# 0.0007489019994864066
ListPrepper.www_checker('domainpurge', 'wwwlist')

# Now delete all dead domains
#import multiproc




