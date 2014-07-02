# README #

qpyman is a tool created to execute queues of jobs and doing all the postprocessing and reporting automatically, making the computer work continuously and giving the user the opportunity to do other things while being informed.

### What is this repository for? ###

* Create computing jobs
* Give them priorities
* Create postprocessing tasks
* Execute everything failure safe
* Send reports by e-mail in real time

### How do I get set up? ###

* Get python and smtplib
* Use savemailinfo.py to save your e-mail account info (I recommend to create a new e-mail account as the password is saved in plain text and if you execute a lot of jobs it may fill your inbox quickly.)
* Create experiments with the provided script.
* Give them priorities in queue.json
* Execute them using qpyman.py

### Who do I talk to? ###

* Any issue, comment, suggestion... send an e-mail to pau.rodri1 at gmail.com
* Mind this is a tool created as an aid for a Computer Science final year project and it hasn't been written clearly.