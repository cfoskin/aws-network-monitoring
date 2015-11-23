#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import boto
import boto.ec2
import time
import os
myInstances = []
key = 'cfoskin_key.pem'

def run_remote_command(cmd):
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

def getAllMyInstances(conn):
 reservations = conn.get_all_reservations()
 global myInstances
 for res in reservations:
     for inst in res.instances:
         if 'Name' in inst.tags:
             if inst.tags['Name'] == 'PA_cFoskin_AS_group':
                 myInstances.append(inst)
 
def listMyInstances(conn):
 getAllMyInstances(conn)#gather my instances and store them in an array
 print('There are %d instances in Colums Autoscale group \n' % len(myInstances))
 if len(myInstances) == 0:
     print('No instances in Colums Autoscale group Please ensure you have instances first')
 else:
     for inst in myInstances:
         print("%s (%s) [%s]" % (inst.tags['Name'], inst.id, inst.state))
        
def check_myInstances_Access_Logs():
 if len(myInstances) == 0:
     print('No instances in Colums Autoscale group Please ensure you have instances first')
 else:
     cmd = "ssh -t -o StrictHostKeyChecking=no -i " + key + " " + "ec2-user@"
     for inst in myInstances:
        print("Connecting to instance :  %s to check the apache access_log file........." % inst.id)
        run_remote_command(cmd + inst.ip_address + " 'sudo cat /var/log/httpd/access_log' ")
        time.sleep(3)

def copy_access_logs_to_local():
 cmd_create_directory = "mkdir access_logs"
 os.system(cmd_create_directory)
 for inst in myInstances:
     cmd_change_owner = "ssh -t -i " + key + " ec2-user@" + inst.ip_address + " sudo chown ec2-user /var/log/httpd/"
     cmd = "scp -i " + key + " ec2-user@"+ inst.ip_address+ ":/var/log/httpd/access_log"+ " ./access_logs"  
     if run_remote_command(cmd_change_owner) == bool(0):
         print("Error with chown")
     else:
         print("Attempting scp to current directory....")
         run_remote_command(cmd)
         os.system("mv ./access_logs/access_log ./access_logs/access_log_%s" % inst.ip_address)
