import util_functions

serial_num = str(util_functions.getserial())  # Serial Number of bike this code is running on
# serial_num = "12345"
f = "./logfile.log"


def email_log_file():
    util_functions.send_event_email(
        "Log",
        "Log files for Bike Serial #" + serial_num,
        attachment=f,
        attachment_name=serial_num + "-logfile.log"
    )
    print "Log file sent"


if __name__ == "__main__":
    email_log_file()
