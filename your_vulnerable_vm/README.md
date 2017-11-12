Instructions to add your Vulnerable VM to NinjaDVA
==================================================

1. Modify / Adapt the Vagrantfile as shown in the example 
2. Modify your VM to submit points to the dashboard VM when some
   participant solved something (see Chapter Submit Solutions)

Submit Solutions
================
To inform the dashboard that a participant solved a challenge, use the installed program 
```
ninjasolver [options]
-r   (required) url of the solution handler script on the dashboard vm
-i   (required) ip address of the participant solved the challenge
-c   (required) category of the solution
-s   (required) state of the challenge
-m   (optional) message for the trainer

Example: 

ninjasolver -r http://dashboard.mgmsp-lab.com/solve_srv.cgi -i 172.23.42.137 -c some_challenge -s 7 -m 'Ben solved something'"
```
