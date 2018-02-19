'''
Mockup of multiprocessing structure for local buffer system

TODO: 
    - put in place the actual buffer instead of 'count' method
    - reroute pinging to the actual server backend instead of google
    
'''

import subprocess
import multiprocessing
import time

# sending data to the cloud 
def ping(): 
    while(1):
        c1 = 'ping google.com -n 1'.split()
        out = subprocess.check_output(c1, shell=True) 
        # out = out.split('\n')
        # target = '' 
        # for line in out: 
        #     if 'Reply' in line: 
        #         target = line 
        print(out)

# local process on local hardware 
def count(): 
    i = 0
    while(1): 
        time.sleep(0.1)
        print(i)
        i += 1
        
def main(): 
    f1 = multiprocessing.Process(target=ping)
    f2 = multiprocessing.Process(target=count) 
    
    f1.start()
    f2.start()
    
if __name__ == "__main__":
    ping() 