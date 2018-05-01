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
        line_stripper(str(infile), str(infile+1), match)
        infile += 1


if __name__ == "__main__":
    with open('progress.txt', 'r') as file:
        loop(file.readlines())