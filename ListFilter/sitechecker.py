import socket
import urllib.request
import urllib.error


def alive_checker(filename, output):
    with open(filename, 'r') as infile, open(output, 'w') as outfile:
        for site in infile:
            # Strip to remove \n character
            website = site.strip()
            # If it resolves, check if it returns http error
            if resolves(website):
                # if it does not return an http error
                if http_error(website):
                    # write to file, it's valid
                    outfile.write(site)


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
    except urllib.error:
        return False


if __name__ == "__main__":
    alive_checker('domains_stripped', 'checked')