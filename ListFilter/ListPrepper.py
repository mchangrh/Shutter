import socket
import urllib.request
import urllib.error
import multiprocessing


def download(site, filename):
    import shutil
    with urllib.request.urlopen(site) as response, open(filename, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def extract(filename):
    import tarfile
    import shutil
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


def hosts_stripper(filename, output):
    with open(filename, 'r') as infile, open(output, 'w') as outfile:
        for line in infile:
            # If hosts file is in 0.0.0.0 format
            if line.startswith('0.0.0.0'):
                newline = line[7:].strip()
            # If hosts file is in 127.0.0.1 format
            elif line.startswith('127.0.0.1'):
                newline = line[9:].strip()
            # If its something else, just pass
            else:
                newline = None
            # Now we write to file
            if newline:
                # Check for local and localhost
                if newline.startswith('local'):
                    pass
                else:
                    outfile.write(newline + '\n')
