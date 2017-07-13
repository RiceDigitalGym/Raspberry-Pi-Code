"""
Helper functions used by other parts of the code.
June 2017

Authors:
Hamza Nauman
Titus Deng
"""
import logging


def getserial():
    """
    Returns the unique integer serial number associated with the raspberry pi
    this code is running on.
    """
    logger = get_logger("Serial")
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')    # Open file that contains serial no.
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]   # Read number from within file.
        f.close()
        return int("0x" + cpuserial, 16)  # Convert from hex to int
    except:                               # Couldn't find file.
        print "Could not find Serial No. of Pi"
        logger.exception("Failed to find Serial Number of Raspberry Pi")
        raise


def get_logger(name):
    """
    Creates a logging object with the given name, setting all the proper file handling and formatting for this
    object. Logging methods can then be called on this logging object.
    """
    logger = logging.getLogger(name)
    level = logging.DEBUG

    logger.setLevel(level)

    # create a file handler
    handler = logging.FileHandler('logfile.log')
    handler.setLevel(level)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  "%d %b %Y %I:%M:%S %p")
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger


# If this file is called by itself (not imported), it will print of the serial number of the pi.
if __name__ == "__main__":
    print getserial()