#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import boto
import boto.ec2
import time
import os
myInstances = []
key = 'cfoskin_key.pem'

# This python module provides functionality such as retrieving instances in my autoscaling group
# and some other features such as generating traffic to the elb using a curl script,
# viewing the access logs for all of my instances and also the option to create a local directory to store them
# and then copy them down and tag them with each instance id

#utility function - using subprocesses, execute various commands
def run_command(cmd):
 (status,output) = subprocess.getstatusoutput(cmd)
 if status >0:
     print("status: %d \n" % status)
     return bool(0)
 else:
     print("status:", status)
     print(output)
     return bool(1)

#opens the connection to the region specified and sets up the reservation
def connect():
    print('Opening connection - Please Wait......')
    conn = boto.ec2.connect_to_region("eu-west-1")
    if conn:
        return conn
        print('Connection Made \n')
    else:
        print('Error: failed to connect to EC2 region')
        sys.exit(1)

#retrieve all my instances
def getAllMyInstances(conn):
 reservations = conn.get_all_reservations()
 global myInstances
 for res in reservations:
     for inst in res.instances:
         if 'Name' in inst.tags:
             if inst.tags['Name'] == 'PA_cFoskin_AS_group':
                 if not inst in myInstances:
                     myInstances.append(inst)
 
#list instances 
def listMyInstances():
 print('There are %d instances in Colums Autoscale group \n' % len(myInstances))
 if len(myInstances) == 0:
     print('No instances in Colums Autoscale group Please ensure you have instances first')
 else:
     index = 0
     for inst in myInstances:
         print("%d %s (%s) [%s]" % (index, inst.tags['Name'], inst.id, inst.state))
         index = index+1

#copy access logs from each instance locally
def copy_access_logs_to_local():
 if len(myInstances) == 0:
      print('No instances in Colums Autoscale group Please ensure you have instances first')
 else:    
     cmd_create_directory = "mkdir access_logs"
     run_command(cmd_create_directory)#make a local dir for them
     for inst in myInstances:
         print("Connecting to instance :  %s to check the apache access_log file........." % inst.id)
         #change owner of httpd dir as its sudo protected
         cmd_change_owner = "ssh -t -i " + key + " ec2-user@" + inst.ip_address + " sudo chown ec2-user /var/log/httpd/"
         cmd = "scp -i " + key + " ec2-user@"+ inst.ip_address+ ":/var/log/httpd/access_log"+ " ./access_logs"  
         print("changing owner of directory prior to SCP.....")
         if run_command(cmd_change_owner) == bool(0):
             print("Error with chown")
         else:
             print("Successful......Attempting SCP to access_logs directory....")
             run_command(cmd)
             #rename each access_log file by tagging it with the id
             os.system("mv ./access_logs/access_log ./access_logs/access_log_%s" % inst.ip_address)

#use curl to generate trafffic to elb - used for examing the algorithm of elb
def generate_traffic_ELB():
 cmd = "./generateTraffic.sh &" 
 print('Executing The generateTraffic.sh script.....')
 os.system(cmd)
 print('Traffic is now being generated using curl...\n')

#script installs siege and runs mimicing 500 users
def use_siege():
 print('Executing The siege.sh script.....')
 cmd_run_siege = "./siege.sh"
 os.system(cmd_run_siege)

#check the logs without copying down
def check_myInstances_Access_Logs():
 if len(myInstances) == 0:
     print('No instances in Colums Autoscale group Please ensure you have instances first')
 else:
     cmd = "ssh -t -o StrictHostKeyChecking=no -i " + key + " " + "ec2-user@"
     for inst in myInstances:
         print("Connecting to instance :  %s to check the apache access_log file.........\n" % inst.id)
         run_command(cmd + inst.ip_address + " 'sudo cat /var/log/httpd/access_log' ")
         print(' Checking the next instance in your group... \n')
         time.sleep(12)#allow time to read them before moving to next

#allow the user to view the network statistics of any instance
def view_instance_stats(cmd):
 index = 0
 for inst in myInstances:
     if inst.state == 'running':
         print("%d %s (%s) [%s]" % (index, inst.tags['Name'], inst.id, inst.state))
         index = index+1 
 choice = input('choose and instance index.. \n\n ') 
 if int(choice) < len(myInstances):
     chosen_instance = myInstances[int(choice)]
     print(chosen_instance.ip_address)
     cmd = "ssh -t -o StrictHostKeyChecking=no -i " + key + " " "ec2-user@" + chosen_instance.ip_address + cmd
     print('connecting .......')
     run_command(cmd)
 else: print('please choose a correct index')   
 
#view networ stats
def view_network_stats():
 cmd = " 'netstat -a' "
 view_instance_stats(cmd)
 
#view vm stats
def virtual_memory_stats():
 cmd = " 'vmstat' "
 view_instance_stats(cmd)