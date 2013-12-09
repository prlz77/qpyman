# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:16:13 2013

@author: prlz77
"""

from config import *
import warning
import datetime
import subprocess, threading
import shutil
import json
import sys
import os

def replace_dir(dst):
    path = os.path.dirname(dst)
    target = os.path.basename(dst)
    basenum = 0
    for d in os.listdir(path):
        if target != '_'.join(d.split('_')[:-1]) and target != d:
            continue
        
        try:
            number = int(d.split('_')[-1])
            basenum = max(number + 1, basenum)
        except:
            basenum = max(1, basenum)
            pass
    
    if basenum > 0:
        dst += '_' + str(basenum)             
    
    return dst
        

                
        

class PySciQ(object):
    def __init__(self):
        self.currExp = None
        self.process = None
        self.queue = None
        self.workDir = os.getcwd()
        self.timeout = False

    def nextExperimentFromQueue(self):
        with open(os.path.join(QUEUE_PATH , "queue.json"),'r') as infile:
            self.queue = json.load(infile)  
        
        name = ''
        if len(self.queue['queue']) > 0:
            name = self.queue['queue'][0]
        else:
            self.queue = None
            name = ''
        
        if name == '':
            allnames = os.listdir(QUEUE_PATH)
            for n in allnames:
                if n != 'queue.json':
                    name = n.split('.json')[0]
                    break
        else:
            self.queue['queue'].pop(0)
            
        if name == '':
            return ''
            
        with open(os.path.join(QUEUE_PATH , name + ".json"),'r') as infile:
            self.currExp = json.load(infile) 
            
        return self.currExp

    def run(self):
        def target():
            os.chdir(self.currExp['path'])
            try:
                self.process = subprocess.Popen(self.currExp['command'].split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, cwd=self.currExp['path'])  
                if self.currExp['timeout'] > 0:   
                    self.timer.start()
                out, error = self.process.communicate()
                
                if self.currExp['timeout'] > 0:                    
                    self.timer.cancel()
                    
                self.currExp['stdout'] = out
                self.currExp['stderr'] = error
                

            except Exception as e:
                print e.message
                print "Invalid command:", sys.exc_info()[0]
                self.currExp['returncode'] = 1 #error
                
                      
        def timer_callback():
            print('Terminating process (timed out)')
            self.process.terminate()
            self.timeout = True

            
        thread = threading.Thread(target=target)
        if self.currExp['timeout'] > 0:  
            self.timer = threading.Timer(self.currExp['timeout'], timer_callback)
        thread.start()
        thread.join()

    def main(self):
        while self.nextExperimentFromQueue() != '':
            if len(os.listdir(PROCESSING_PATH)) > 0:
                e = Exception()
                e.message = "Problem occurred, another experiment is being processed"
                print e.message
                raise e
                sys.exit()
            
            self.currExp['returncode'] = 1    
            self.currExp['stdout'] = ''
            self.currExp['stderr'] = ''  
            self.timeout = False
            
            dirname = os.path.join(PROCESSING_PATH, self.currExp['name'])
            os.mkdir(dirname)
            src = os.path.join(QUEUE_PATH, self.currExp['name'] + '.json')
            dst = os.path.join(PROCESSING_PATH, self.currExp['name'])
            try:
                shutil.move(src, dst)
            except:
                print "Warning: 
            if self.queue != None:
                with open(os.path.join(QUEUE_PATH, 'queue.json'), 'w') as outfile:
                    json.dump(self.queue, outfile)
            start = str(datetime.datetime.now())
            self.run()
            finish = str(datetime.datetime.now())
            
            self.currExp['returncode'] = self.process.returncode            
            if self.timeout:
                self.currExp['returncode'] = -50
            
            os.chdir(self.workDir)   
            src = os.path.join(PROCESSING_PATH, self.currExp['name'])
            dst = os.path.join(COMPLETED_PATH, self.currExp['name'])
            dst = replace_dir(dst)                  
            shutil.move(src, dst)

            self.currExp['start'] = start
            self.currExp['finish'] = finish
            
            filename = os.path.join(dst, self.currExp['name'] + '_results.json')
            with open(filename, 'w') as outfile:
                json.dump(self.currExp, outfile)
            
            ps = self.currExp['postscript']
            if ps != "":
                subprocess.call(ps.split() + [os.path.abspath(dst), self.currExp['name']])
               
                
        
if __name__ == '__main__':
    ps = PySciQ()
    ps.main()

        
