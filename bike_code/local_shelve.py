from __future__ import print_function

import os
import shelve
import subprocess
import multiprocessing


class LocalShelve(object):
    def __init__(self, filename):
        '''
        initialization
        :param filename: it is recommended that the filename does not have an extension, a '.db' extension will be automatically added.
        :return: None
        '''
        self.filename = filename
        self.db = shelve.open(self.filename, writeback=True)
        self.keyVals = ['serialNumber', 'status', 'rpm', 'RFID']
        self._init_empty_shelve()

    def __len__(self):
        return len(self.db['serialNumber'])

    def print(self):
        for k in self.keyVals:
            print(k, self.db[k])

    def _init_empty_shelve(self):
        for k in self.keyVals:
            self.db[k] = []

    def add_entry(self, data):
        '''
        add_entry - add a entry to the current d
        :param data: a dictionary object, such as: {'serialNumber':12345, 'status': 'alive', 'rpm': 90, 'RFID':0x90}
        :return: None
        '''
        if list(data.keys()).sort() != list(self.keyVals).sort():
            print("Wrong Data.")
            print(self.keyVals)
            print(data.keys())
            raise KeyError('Data has unrecognized key values, which LocalShelve did not got initialized with.')
        else:
            for k in self.keyVals:
                self.db[k].append(data[k])
        self.db.sync()

    def pop_entry(self):
        # this modifies the database
        out_data = {}.fromkeys(self.keyVals)
        for k in self.keyVals:
            out_data[k] = self.db[k].pop(0)
        self.db.sync()
        return out_data

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


# a = LocalShelve('test_db.db')
# a.add_entry({'serialNumber': 12345, 'status': 'alive', 'rpm': 90, 'RFID': 0x90})
# a.add_entry({'serialNumber': 12346, 'status': 'alive', 'rpm': 56, 'RFID': 0x90})
# a.add_entry({'serialNumber': 12347, 'status': 'alive', 'rpm': 80, 'RFID': 0x90})
# # print(len(a))
# print(a.print())
# print(a.pop_entry())
# print(a.print())
# a.end_session()

#
# a = {'serialNumber': [12345, 12345, 12345], 'status': ['alive', 'alive', 'alive'], 'rpm': [90, 56, 80], 'RFID': [0x90, 0x90, 0x90]}
#
# up = Uploader(dir_path='queue')
# up.sequential_upload()
#













