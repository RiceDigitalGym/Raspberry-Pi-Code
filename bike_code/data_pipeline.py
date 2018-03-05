import local_shelve
import subprocess
import multiprocessing
import numpy as np

localdb = local_shelve.LocalShelve('local_buffer.db')
has_internet = True

# sending data to the cloud
def data_collect():
    rpm = randint(low=10, high=250)
    data = {'serialNumber': 12345, 'status': 'alive', 'rpm': rpm, 'RFID': 0x90}
    return data

def send_data(data):
    try:
        # send data to cloud
        c1 = 'ping google.com -n 1'.split()
        out = subprocess.check_output(c1, shell=True)
        has_internet = True
    except Exception as e:
        has_internet = False
        print(e)
        # sending to cloud failed.
        # storing locally
        localdb.add_entry(data)

# local process on local hardware
def local_database(data):
    '''
    takes in data while the service is down
    :return:
    '''
    while has_internet is False:
        localdb.add_entry(data)


def main():
    f1 = multiprocessing.Process(target=send_data, args=(data))
    f2 = multiprocessing.Process(target=local_database)
    while True:
        d = data_collect()
        f1.start()
        f2.start()

        # Exit the completed processes
        f1.join()
        f2.join()


if __name__ == "__main__":
    main()
