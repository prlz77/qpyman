# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 19:47:00 2013

@author: pc
"""
import json

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class SendMail:
    def __init__(self):
        try:
            with open(".mailinfo.json",'r') as infile:
                self.mailinfo = json.load(infile)  
        except IOError:
            print ".mailinfo.json not found. Use savemailinfo.py to generate it"
    def send(self, header, body, images = []):
        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'html'))
        
        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = header
        msg['From'] = self.mailinfo['orig']
        msg['To'] = self.mailinfo['dest'][0]
        
        # Assume we know that the image files are all in PNG format
        for image in images:
            # Open the files in binary mode.  Let the MIMEImage class automatically
            # guess the specific image type.
            fp = open(image, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP(self.mailinfo['server'])
        s.sendmail(self.mailinfo['orig'], self.mailinfo['dest'], msg.as_string())
        s.quit()