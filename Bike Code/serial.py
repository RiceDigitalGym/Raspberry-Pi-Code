"""
Code to get the Serial Number of Raspberry Pi.
June 2017
"""


def getserial():
    """
	Returns the unique integer serial number associated with the raspberry pi 
	this code is running on.
	"""
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')  # Open file that contains serial no.
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]  # Read number from within file.
        f.close()
    except:
        print "Could not find Serial No. of Pi"
        cpuserial = "ERROR000000000"  # Couldn't find file.
    return int("0x" + cpuserial, 16)  # Convert from hex to int

print getserial()