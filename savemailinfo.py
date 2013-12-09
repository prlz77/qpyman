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

    mail = {}
    
    print "Enter smtp server"
    mail['server'] = raw_input()
    if mail['server'] == '':
        print "Server must not be empty"
        sys.exit()
    
    print "\nEnter sender direction"
    mail['orig'] = raw_input()
    if mail['orig'] == '':
        print "Sender must not be empty"
        sys.exit()

    print "\nEnter destinatary direction"
    mail['dest'] = [raw_input()]
    if mail['dest'] == '':
        print "Dest must not be empty"
        sys.exit()
                             
    with open('.mailinfo.json','w') as outfile:
        json.dump(mail,outfile) 
        print "Saved."         
    
