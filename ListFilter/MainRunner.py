import ListPrepper

# Download and extract files
ListPrepper.extract()

# Delete all IP addresses
ListPrepper.strip_all_ip('domains', 'ippurge')

# Strip all domains matching site list
ListPrepper.domain_stripper('ippurge', 'domainpurge')

# add www version if it applies
ListPrepper.www_checker('domainpurge', 'wwwlist')


# Now delete all dead domains
# import multiproc
# do this however you want



