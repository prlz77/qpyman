# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:24:21 2013

@author: prlz77
"""

from config import *
import json
import sys
import os


if __name__ == '__main__':

    experiment = {}
    
    print "Enter experiment name"
    experiment['name'] = raw_input()
    if experiment['name'] == '':
        print "Name must not be empty"
        sys.exit()
    
    print "\nEnter description"
    experiment['description'] = raw_input()
    
    print "\nEnter full working directory path"
    experiment['path'] = raw_input()

    print "\nEnter command"
    experiment['command'] = raw_input()
        
    print "\nEnter timeout (default = 0 seconds)"
    timeout = raw_input()
    if timeout != "":
        try:
            experiment['timeout'] = int(timeout)
        except ValueError:
            print "Could not convert data to an integer."
            sys.exit()
            
    else:
        experiment['timeout'] = 0
        
    print "\nSend mail when finished? y/n (default is y)"
    answer = raw_input()
    if answer in ['N','n']:
        experiment['mail'] = 0
    else:
        experiment['mail'] = 1
  
           
    print "\nPostprocessing Script (will receive 0 if correct execution or 1 if error occurred):"     
    experiment['postscript'] = raw_input()
        
    with open(os.path.join(QUEUE_PATH , "queue.json"),'r') as infile:
        queue=json.load(infile)  
        
    for index,element in enumerate(queue['queue']):
        if experiment['name'] == element['name']:
            print "Experiment name already exists, replace?"
            answer = raw_input()
            if answer != '' and answer[0] in ['N','n']:
                sys.exit()
            else:
                queue['queue'].pop(index)
                break
        
    queue['queue'].append(experiment['name'])
    
    with open(os.path.join(QUEUE_PATH, 'queue.json'),'w') as outfile:
        json.dump(queue,outfile)          
    with open(os.path.join(QUEUE_PATH, experiment['name'] + '.json'),'w') as outfile:
        json.dump(experiment,outfile)     
