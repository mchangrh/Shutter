import socket
import urllib.request
import urllib.error


class Checker:
    def __init__(self, infile, outfile, deadfile):
        self.infile = open(infile, 'r')
        self.outfile = open(outfile, 'a')
        self.dead = open(deadfile, 'a')
        self.name = infile

    def pass_checker(self):
        # Implement dead and alive counter
        alive_count, dead_count = 0, 0
        for site in self.infile:
            website = site.strip()
            valid = False
            if Checker.resolves(website):
                valid = Checker.http_error(website)
            # check for valid
            if valid:
                alive_count += 1
                self.outfile.write(site)
            else:
                print(self.name + " dead " + str(dead_count + alive_count) + "  " + website)
                dead_count += 1
                self.dead.write(site)
        print(self.name + " alive: " + str(alive_count) + " dead: " + str(dead_count))

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

    def close(self):
        self.infile.close()
        self.outfile.close()
        self.dead.close()

"""
if __name__ == "__main__":
    filename = "custom_aa"
    pass_one = Checker(filename, filename + "pass1", filename + "dead1")
    pass_one.pass_one()
    pass_one.close()
"""
