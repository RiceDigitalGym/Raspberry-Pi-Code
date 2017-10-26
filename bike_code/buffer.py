'''
Tries to send RPM info from the bike directly to online if the POST 
request is successful (i.e. 500). If an error (i.e. 404) is received, 
send to local buffer while simultaneously attempting to offload 
buffered data to online. 

Alternatively, constantly send the information to the local buffer 
and simultaneously attempt to send to server regardless of 500/404. 

'''

from multiprocessing import Process
from __future__ import print_function
import os
import shelve
import requests 

# Define the API endpoint:
API_ENDPOINT = "http://52.34.141.31:8000/bbb/bike"
API_START_WORKOUT = "http://52.34.141.31:8000/bbb/start_workout"
API_END_WORKOUT = "http://52.34.141.31:8000/bbb/end_workout"


def process_data(data, shelf):
	'''
	Sends the given data to a given LocalShelve object while attempting to send to server. 
	'''
	def send_rpm(post_data):
		r = requests.post(url=API_ENDPOINT, data=post_data)
		return r.status_code
	
	def send_first_to_server(shelf):
		'''
		Tries to send the first entry in the LocalShelve to server. 
		If sending is successful, then remove that entry from the LocalShelve. 
		'''
		buffer = shelf.open(shelf)
		# extract each column of data from buffer - serials, statuses, rpms, and rfids 
		serials = buffer['serialNumber']
		statuses = buffer['status']
		rpms = buffer['rpm'] 
		rfids = buffer['RFID']
		# format the first entry as POST data 
		first_entry = {'serialNumber': serials[1], 'statuses': statuses[1], 
			'rpm': rpms[1], 'RFID': rfids[1]}
		# send the first entry. if the response is ok, then remove the entry from the buffer. 
		# do this by placing back all entries minus the first into the shelf. 
		if send_rpm(first_entry) == requests.codes.ok: 
			
		

class LocalShelve(object):
    def __init__(self, filename):
        '''
        initialization
        :param filename: it is recommended that the filename does not have an extension, a '.db' extension will be automatically added.
        :return: None
        '''
        self.filename = filename
        self.db = shelve.open(self.filename)
        self.keyVals = ['serialNumber', 'status', 'rpm', 'RFID']
        self._init_empty_shelve()

    def _init_empty_shelve(self):
        for k in self.keyVals:
            self.db[k] = []

    def add_entry(self, data):
        '''
        add_entry - add a entry to the current d
        :param data: a dictionary object, such as: {'serialNumber':12345, 'status': 'alive', 'rpm': 90, 'RFID':0x90}
        :return: None
        '''
        if data.keys().sort() != self.keyVals.sort():
            print(self.keyVals)
            print(data.keys())
            raise KeyError('Data has unrecognized key values, which LocalShelve did not get initialized with.')
        else:
            for k in self.keyVals:
                self.db[k].append(data[k])

    def end_session(self):
        self.db.close()

class Uploader(object):
    def __init__(self, dir_path):
        self.dir = os.path.abspath(dir_path)
        self.collections = [x for x in os.listdir(self.dir) if x.endswith(".db")]
        self.flag = False

    def sequential_upload(self):
        '''
        sequential_upload - sequentially upload each file in the directory
        :return:
        '''
        if len(self.collections) == 0:
            print('[WARNING] No items found. Is this the right directory?')
        for item in self.collections:
            # we do this b/c DbfilenameShelf instance has no attribute '__exit__'
            db = shelve.open(item)
            # TODO: NEED HAMZA TO PLUG IN UPLOADER CODE.
            print('[INFO] Uploading', item)
            db.close()
        print('[INFO] Upload successfully finished.')
        self.flag = True

    def clean_dir(self):
        if self.flag is True:
            for f in self.collections:
                os.remove(f)


# Driver code to test local_shelve module
def main():
	a = LocalShelve(os.path.join('queue', 'test2.db'))
	a.add_entry({'serialNumber': 12345, 'status': 'alive', 'rpm': 90, 'RFID': 0x90})
	a.add_entry({'serialNumber': 12345, 'status': 'alive', 'rpm': 56, 'RFID': 0x90})
	a.add_entry({'serialNumber': 12345, 'status': 'alive', 'rpm': 80, 'RFID': 0x90})
	a.end_session()

	a = {'serialNumber': [12345, 12345, 12345], 'status': ['alive', 'alive', 'alive'], 'rpm': [90, 56, 80], 'RFID': [0x90, 0x90, 0x90]}

	up = Uploader(dir_path='queue')
	up.sequential_upload()