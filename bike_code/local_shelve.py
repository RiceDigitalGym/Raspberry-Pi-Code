from __future__ import print_function

import os
import shelve


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
            raise KeyError('Data has unrecognized key values, which LocalShelve did not got initialized with.')
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


#
# a = LocalShelve(os.path.join('queue', 'test2.db'))
# a.add_entry({'serialNumber': 12345, 'status': 'alive', 'rpm': 90, 'RFID': 0x90})
# a.add_entry({'serialNumber': 12345, 'status': 'alive', 'rpm': 56, 'RFID': 0x90})
# a.add_entry({'serialNumber': 12345, 'status': 'alive', 'rpm': 80, 'RFID': 0x90})
# a.end_session()
#
# up = Uploader(dir_path='queue')
# up.sequential_upload()














