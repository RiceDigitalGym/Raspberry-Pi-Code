import smtplib
import time
import util_functions
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

me = "digital.gym.alert@gmail.com"            # Email address for sender
target = "hn9@rice.edu"                       # Email address for recipient
server = smtplib.SMTP("smtp.gmail.com", 587)  # Initiate Email Server
serial_num = util_functions.getserial()               # Serial Number of bike this code is running on
# serial_num = "12345"
f = "../logfile.log"


def send_now():
    msg = MIMEMultipart()

    msg["Subject"] = "Log files for Bike Serial #" + str(serial_num)
    msg["From"] = me
    msg["To"] = target

    now_date = time.strftime("%x")  # Current Date
    now_time = time.strftime("%X")  # Current Time

    # Main text of email.
    text = "Date: " + now_date + "\n" + \
           "Time: " + now_time + "\n"

    msg.attach(MIMEText(text))

    with open(f, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=(str(serial_num) + "-" + basename(f))
        )
        part['Content-Disposition'] = 'attachment; filename="%s"' % (str(serial_num) + "-" +basename(f))
        msg.attach(part)

    server.starttls()
    server.login(me, "ashu1234")  # Login into sender email address
    server.sendmail(me, target, msg.as_string())
    server.quit()
    print "Log file sent"


if __name__ == "__main__":
    send_now()
