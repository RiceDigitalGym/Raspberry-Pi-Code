"""
Helper functions used by other parts of the code.
June 2017

Authors:
Hamza Nauman
Titus Deng
"""
import smtplib
import logging
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

me = "digital.gym.alert@gmail.com"            # Email address for sender
target = "rice.sensor@gmail.com"              # Email address for recipient


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


def send_event_email(event, subject, logger=None, attachment=None, attachment_name=None):
    """
    Sends an email to the target email specifying the time and date of an event.
    An attachment can also optionally be sent.
    :param event: Name of event that has occurred.
    :param subject: Subject of email to send.
    :param logger: Optional logger object to log the success/failure of sending the email.
    :param attachment: Path of the optional attachment file.
    :param attachment_name: Name of the optional attachment file that should be shown in the email
    """
    now_date = time.strftime("%x")  # Current Date
    now_time = time.strftime("%X")  # Current Time

    # Main text of email.
    text = event + " Date: " + now_date + "\n" + \
           event + " Time: " + now_time + "\n"

    msg = MIMEMultipart()

    msg["Subject"] = subject
    msg["From"] = me
    msg["To"] = target

    msg.attach(MIMEText(text))

    if attachment is not None and attachment_name is not None:
        with open(attachment, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=attachment_name
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % attachment_name
            msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Initiate Email Server
        server.starttls()
        server.login(me, "ashu1234")  # Login into sender email address
        server.sendmail(me, target, msg.as_string())
        if logger is not None:
            logger.info("Successfully sent email for event: \'" + event + "\'")
        print "Sent email for event: \'" + event + "\'"
        server.quit()
    except smtplib.SMTPException:
        if logger is not None:
            logger.exception("Failed to send email for event: \'" + event + "\'")
        print "Failed to send email for event: \'" + event + "\'"


# If this file is called by itself (not imported), it will print of the serial number of the pi.
if __name__ == "__main__":
    print getserial()
