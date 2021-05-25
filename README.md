# ccc-assmt2

# Twitter Harvester
If you would like to run the program locally, direct to the folder first.  
`cd ccc-assmt2/Harvester`   
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
`cd ccc-assmt2/MapReduce` 

Then the program could be run as:  
`python MapReduce.py -n <The name of the design document, no special requirement> -s <The ip address of the server, in the form of http://admin:password@ip:5984/> -p <The purpose of using mapreduce, please follow the help information> -d <The name of the database which will be visited>`  

If you still have questions, please type `python MapReduce.py -h` to check the help.
