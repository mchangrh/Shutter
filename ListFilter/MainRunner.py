import ListPrepper


def ut1():
    # Download and extract files
    site = "ftp://ftp.ut-capitole.fr/pub/reseau/cache/squidguard_contrib/adult.tar.gz"
    filename = "adult.tar.gz"
    ListPrepper.download(site, filename)
    ListPrepper.extract(filename)

    # Delete all IP addresses
    ListPrepper.strip_all_ip('domains', 'ippurge')

    # Strip all domains matching site list
    ListPrepper.domain_stripper('ippurge', 'domainpurge')

    # add www version if it applies
    ListPrepper.www_checker('domainpurge', 'wwwlist')

    # Now delete all dead domains
    # import multiproc
    # do this however you want


def sinfonietta():
    # Download file
    site = 'https://raw.githubusercontent.com/Sinfonietta/hostfiles/master/pornography-hosts'
    filename = 'sin_hosts'
    ListPrepper.download(site, filename)
    ListPrepper.hosts_stripper(filename, filename+'nohost')
    ListPrepper.domain_stripper(filename + 'nohost', filename + 'dpurge')
    # Now delete all dead domains
    # import multiproc
    # do this however you want


def clefspeare():
    # Download file
    site = 'https://raw.githubusercontent.com/Clefspeare13/pornhosts/master/0.0.0.0/hosts'
    filename = 'clef_hosts'
    ListPrepper.download(site, filename)
    ListPrepper.hosts_stripper(filename, filename+'nohost')
    ListPrepper.domain_stripper(filename + 'nohost', filename + 'dpurge')
    # Now delete all dead domains
    # import multiproc
    # do this however you want
