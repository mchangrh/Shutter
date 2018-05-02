import socket
import urllib.request
import urllib.error


def extract():
    import tarfile
    import shutil
    filename = "adult.tar.gz"
    site = "ftp://ftp.ut-capitole.fr/pub/reseau/cache/squidguard_contrib/adult.tar.gz"
    with urllib.request.urlopen(site) as response, open(filename, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    # Extract all files
    tar = tarfile.open(filename, "r:gz")
    tar.extractall()
    # Clean up the extra mess we made
    shutil.move('adult/domains', 'domains')
    shutil.rmtree('adult')


def check_noip(address):
    try:
        socket.inet_aton(address)
        # works
        return False
    except socket.error:
        # domain
        return True


def strip_all_ip(filename, output):
    # open files
    with open(filename, 'r') as infile, open(output, 'w') as outfile:
        # loop through lines
        for line in infile:
            # Strip to avoid \n
            line_strip = line.strip()
            # Check that it is a domain
            if check_noip(line_strip):
                outfile.write(line)


def domain_stripper(filename, output):
    """
    This function strips lines with any of the matched words
    :param filename: Input filename
    :param output: Output filename
    """
    # Open sitelist ban
    sitelist = ['tumblr.com',
                'blogspot.ae', 'blogspot.al', 'blogspot.am', 'blogspot.ba', 'blogspot.ca'
                'blogspot.bg', 'blogspot.ch', 'blogspot.cl', 'blogspot.co.at', 'blogspot.co.id'
                'blogspot.be', 'blogspot.co.at', 'blogspot.co.il', 'blogspot.co.ke', 'blogspot.co.nz'
                'blogspot.co.uk', 'blogspot.co.za', 'blogspot.com.ar', 'blogspot.com.au', 'blogspot.com.br'
                'blogspot.com.by', 'blogspot.com.au', 'blogspot.com.br', 'blogspot.com.by', 'blogspot.com.co'
                'blogspot.com.cy', 'blogspot.com.ee', 'blogspot.com.eg', 'blogspot.com.es', 'blogspot.com.mt'
                'blogspot.com.ng', 'blogspot.com.tr', 'blogspot.com.uy', 'blogspot.cz', 'blogspot.de'
                'blogspot.dk', 'blogspot.fi', 'blogspot.fr', 'blogspot.gr', 'blogspot.hk'
                'blogspot.hr', 'blogspot.com.ar', 'blogspot.hu', 'blogspot.ie', 'blogspot.in'
                'blogspot.is', 'blogspot.it', 'blotspot.jp', 'blogspot.kr', 'blogspot.li'
                'blogspot.lt', 'blogspot.lu', 'blogspot.md', 'blogspot.mk', 'blogspot.mx'
                'blogspot.my', 'blogspot.nl', 'blogspot.no', 'blogspot.pe', 'blogspot.pt'
                'blogspot.qa', 'blogspot.ro', 'blogspot.rs', 'blogspot.ru', 'blogspot.se'
                'blogspot.sg', 'blogspot.sk', 'blogspot.si', 'blogspot.sn', 'blogspot.tw'
                'blogspot.ug', 'blogspot.com']
    # Open files to trim
    with open(filename, 'r') as infile, open(output, 'w') as outfile:
        # Loop through files
        for line in infile:
            # if the line matches any of the sites
            if any(site in line for site in sitelist):
                # write to file
                outfile.write(line)


def www_checker(filename, output):
    with open(filename, 'r') as infile, open(output, 'w') as outfile:
        for line in infile:
            if not line.startswith("www."):
                outfile.write("www." + line)
            # Write either way
            outfile.write(line)


class SiteChecker:
    def __init__(self, infile, outfile, deadfile):
        self.infile = open(infile, 'r')
        self.outfile = open(outfile, 'a')
        self.dead = open(deadfile, 'a')
        self.name = infile

    def pass_checker(self, checker):
        """
        This function checks if a site is dead or alive using 1 of 2 methods
        :param checker: Which checker to use
        """
        # Implement dead and alive counter
        alive_count, dead_count = 0, 0
        # Loop through all sites in list
        for site in self.infile:
            # Strip newlines
            website = site.strip()
            # Set valid to False
            valid = False
            # Two types of checkers
            if checker == "resolves":
                valid = SiteChecker.resolves(website)
            elif checker == "http_error":
                valid = SiteChecker.http_error(website)
            # check for validity
            if valid:
                # Write site to pass_file if valid
                alive_count += 1
                self.outfile.write(site)
            else:
                # Print dead status and write site to dead_file
                print(self.name + " dead " + str(dead_count + alive_count) + "  " + website)
                dead_count += 1
                self.dead.write(site)
        # Print the result of the list
        print(self.name + "  " + checker + " alive: " + str(alive_count) + " dead: " + str(dead_count))

    def pass_one(self):
        """
        This function just runs pass_one
        :return:
        """
        self.pass_checker("resolves")

    def pass_two(self):
        """
        This function just runs pass_two
        :return:
        """
        self.pass_checker("http_error")

    @staticmethod
    def resolves(site):
        """
        This function returns True if the website resolves
        :param site: domain to check
        :return: bool
        """
        # Try resolving with DNS
        try:
            socket.gethostbyname(site)
            return True
        # If it does not resolve
        except socket.error:
            return False

    @staticmethod
    def http_error(site):
        """
        This function returns True if the website returns a valid http status code
        :param site: domain to check
        :return: bool
        """
        # urllib requires a url type
        site = "http://" + site
        # Get HTTP response from urllib
        try:
            response = urllib.request.urlopen(site).getcode()
            # Normal HTTP responses are less than 400
            if response <= 400:
                return True
            # We received an abnormal HTTP response code
            else:
                return False
        # Catch all urllib errors
        except urllib.error.HTTPError:
            return False
        except urllib.error.URLError:
            return False
        except Exception:
            return False

    def close(self):
        """
        This function just closes all the files
        :return:
        """
        self.infile.close()
        self.outfile.close()
        self.dead.close()