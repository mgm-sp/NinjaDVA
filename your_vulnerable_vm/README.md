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
-r, --remote_solution_handler_url  (required) url of the solution handler script on the dashboard vm
-i, --ip_addr                      (required) ip address of the participant solved the challenge
-c, --category                     (required) category of the solution
-s, --state                        (required) state of the challenge
--comment                          (optional) comment for the trainer

Example: 

ninjasolver -r http://dashboard.mgmsp-lab.com/solve_srv.cgi -i 172.23.42.1 -c your_vm_xss1
    -s 10 --comment "He read the mails of Mr. Schmidt"
```
