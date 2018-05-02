import socket
import urllib.request
import urllib.error


class Extractor:
    pass


class DomainFilter:
    """
    This class has functions to clean p repeat domains
    """
    @staticmethod
    def line_stripper(filename, output, match):
        """
        This function strips lines with the matched word
        :param filename: Input filename
        :param output: Output filename
        :param match: Word to match
        :return:
        """
        # Open files
        with open(filename, 'r') as infile, open(output, 'w') as outfile:
            # Loop through files
            for line in infile:
                # If the line does not match, write to out
                if match not in line:
                    outfile.write(line)

    @staticmethod
    def loop(array):
        """
        This function loops through multiple words for stripping
        :param array: list of phrases to match
        :return:
        """
        # Start the infile name at 1
        infile = 1
        for match in array:
            # Increment filename by 1 each time to show iterations
            DomainFilter.line_stripper(str(infile), str(infile + 1), match)
            infile += 1

    @staticmethod
    def loop_from_file(filename):
        # Open file
        with open(filename, 'r') as file:
            # Loop with all lines in file
            DomainFilter.loop(file.readlines())


class SiteChecker:
    """
    This class contains functions that check if a website is valid
    """
    @staticmethod
    def alive_checker(filename, output):
        """
        This function checks all the domains in the given file
        :param filename: Input filename
        :param output: Output filename
        :return:
        """
        with open(filename, 'r') as infile, open(output, 'w') as outfile:
            for site in infile:
                # Strip to remove \n character
                website = site.strip()
                # If it resolves, check if it returns http error
                if SiteChecker.resolves(website):
                    # if it does not return an http error
                    if SiteChecker.http_error(website):
                        # write to file, it's valid
                        outfile.write(site)

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


class Formatter:
    @staticmethod
    def www_checker(filename, output):
        with open(filename, 'r') as infile, open(output, 'w') as outfile:
            for line in infile:
                if not line.startswith("www."):
                    outfile.write("www." + line)
                else:
                    outfile.write(line)
