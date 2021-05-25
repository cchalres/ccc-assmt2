# ccc-assmt2

# Ansible
1.	Get your Openstack Password (openrc.sh) from the dashboard of MRC.
2.	Reset API password and copy the latest password. 
3.	Go to the ansible directory on your computer and Deploy instances on the Nectar.
`cd COMP90024/ccc-assmt2/Ansible`   
You coudl change the configuration files (/hosts_vars/instances.yaml) which include:  
- number of instances
- instance image
- volumes size per instance etc.

Then configure :  
`python Harvester.py -c <Your configuration file> -s <Your server's ip address>`  

If you still have questions, please type `python Harvester.py -h` to check the help.

# Twitter Harvester
If you would like to run the program locally, direct to the folder first.  
`cd COMP90024/ccc-assmt2/Harvester`   
Then you should change the configuration files which include:  
- TwitterAPI credential
- database name
- database's admin and password  

Then the Harvester could be run as:  
`python Harvester.py -c <Your configuration file> -s <Your server's ip address>`  

If you still have questions, please type `python Harvester.py -h` to check the help.

# MapReduce
While this section contains:
- Python script for building views on couchDB
- In ths same script, the views of couchDB for analysis
- Output the dataframe of the query result.  

If you want to run the python script, you need to direct to the folder also.  
`cd COMP90024/ccc-assmt2/MapReduce` 

Then the program could be run as:  
`python MapReduce.py -n <The name of the design document, no special requirement> -s <The ip address of the server, in the form of http://admin:password@ip:5984/> -p <The purpose of using mapreduce, please follow the help information> -d <The name of the database which will be visited>`  

If you still have questions, please type `python MapReduce.py -h` to check the help.

# Web Hosting
The web application is based on Flask and will use NginX as our web server with the support of uWSGI.
In this part, it is mainly forcus on configuration of web server to host the web application, the steps will be shown on the following.

Step 1: 

`sudo systemctl start myproject`

Step 2: 

`sudo systemctl enable myproject`

Step 3:

`sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled`

Step 4:

`sudo nginx -t`

Step 5:

`sudo systemctl restart nginx`

Now the web server has been restarted and with running web application made by ourselves. And it could be seen by typing the IP address into broswer.
