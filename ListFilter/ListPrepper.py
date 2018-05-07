import socket
import urllib.request
import urllib.error
import multiprocessing


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
    sitelist = ['tumblr.com', 'blogspot.']
    # Open files to trim
    with open(filename, 'r') as infile, open(output, 'w') as outfile:
        # Loop through files
        for line in infile:
            # if the line does not match any sites
            if not(any(site in line for site in sitelist)):
                # write to file
                outfile.write(line)


def www_checker(filename, output):
    with open(filename, 'r') as infile, open(output, 'w') as outfile:
        for line in infile:
            # Write a file with just more www
            if not line.startswith("www."):
                outfile.write("www." + line)

class SiteChecker:
    def __init__(self, infile, outfile, deadfile):
        self.infile = open(infile, 'r')
        self.outfile = open(outfile, 'a')
        self.dead = open(deadfile, 'a')
        self.name = infile

        # Processes
        num_procs = 4
        # Create queue
        self.queue = multiprocessing.JoinableQueue()
        procs = []
        for i in range(num_procs):
            procs.append(multiprocessing.Process(target=SiteChecker.worker(self)))
            procs[-1].daemon = True
            procs[-1].start()

        SiteChecker.pass_checker(self)

        self.queue.join()

        for p in procs:
            self.queue.put(None)

        self.queue.join()

        for p in procs:
            p.join()

        # finished
        self.close()

    def pass_checker(self):
        """
        This function checks if a site is dead or alive using 1 of 2 methods
        """
        # Implement dead and alive counter
        alive_count, dead_count = 0, 0
        # Loop through all sites in list
        for site in self.infile:
            # Strip newlines
            self.queue.put(site)
        # Print the result of the list
        print(self.name + " alive: " + str(alive_count) + " dead: " + str(dead_count))

    # Function to actually do work
    def do_work(self, site):
        website = site.strip()
        # Set valid to False
        valid = False
        # Two types of checkers
        if SiteChecker.resolves(website):
            if SiteChecker.http_error(website):
                valid = True
        if valid:
            # Write site to pass_file if valid
            self.outfile.write(site)
        else:
            # Print dead status and write site to dead_file
            self.dead.write(site)
        self.outfile.flush()
        self.dead.flush()

    # Worker function
    def worker(self):
        for site in iter(self.queue.get, None):
            # pass in filename
            print('start' + site)
            self.do_work(site)
            #done
            print('done' + site)
            # finish task
            self.queue.task_done()
        self.queue.task_done()

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
