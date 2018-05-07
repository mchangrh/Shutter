import multiprocessing
import socket
import urllib.request
import urllib.error


class multiproc:
    def __init__(self, open_name):
        # counters
        self.deadcount = 0
        self.alivecount = 0
        # Processes
        num_procs = 8
        # start up files
        self.infile = open(open_name, 'r')
        self.outfile = open(open_name + 'pass', 'a')
        self.dead = open(open_name + 'dead', 'a')
        # Create queue
        self.queue = multiprocessing.JoinableQueue()
        self.procs = []
        for i in range(num_procs):
            self.procs.append(multiprocessing.Process(target=self.worker))
            self.procs[-1].daemon = True
            self.procs[-1].start()
        for site in self.infile:
            self.queue.put(site)
        # Run queue
        self.queue.join()

        for p in self.procs:
            self.queue.put(None)

        self.queue.join()

        for p in self.procs:
            p.join()

        print("FINISHED")
        print('alive: ' + str(self.alivecount))
        print('dead: ' + str(self.deadcount))
        # Finish
        self.infile.close()
        self.outfile.close()
        self.dead.close()

    def check_both(self, site):
            website = site.strip()
            valid = False
            if multiproc.resolves(website):
                if multiproc.http_error(website):
                    valid = True
            # check for valid
            if valid:
                print(str(self.alivecount + self.deadcount) + " alive " + website,)
                self.alivecount += 1
                self.outfile.write(site)
                self.outfile.flush()
            else:
                print(str(self.alivecount + self.deadcount) + " dead " + website)
                self.deadcount += 1
                self.dead.write(site)
                self.dead.flush()

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
            else:
                return False
        except urllib.error.HTTPError:
            return False
        except urllib.error.URLError:
            return False
        except Exception:
            return False

    # Worker function
    def worker(self):
        for name in iter(self.queue.get, None):
            # pass in site
            self.check_both(name)
            # finish task
            self.queue.task_done()
        self.queue.task_done()
