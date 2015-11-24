#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import boto
import boto.ec2
import boto.ec2.autoscale
from boto.ec2.autoscale import ScalingPolicy
from boto.sns import connect_to_region
from boto.ec2.cloudwatch import connect_to_region
from boto.ec2.elb import ELBConnection
import time
import os
myInstances = []
key = 'cfoskin_key.pem'

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

def copy_access_logs_to_local():
 if len(myInstances) == 0:
      print('No instances in Colums Autoscale group Please ensure you have instances first')
 else:    
     cmd_create_directory = "mkdir access_logs"
     run_command(cmd_create_directory)
     for inst in myInstances:
         print("Connecting to instance :  %s to check the apache access_log file........." % inst.id)
         cmd_change_owner = "ssh -t -i " + key + " ec2-user@" + inst.ip_address + " sudo chown ec2-user /var/log/httpd/"
         cmd = "scp -i " + key + " ec2-user@"+ inst.ip_address+ ":/var/log/httpd/access_log"+ " ./access_logs"  
         print("changing owner of directory prior to SCP.....")
         if run_command(cmd_change_owner) == bool(0):
             print("Error with chown")
         else:
             print("Successful......Attempting SCP to access_logs directory....")
             run_command(cmd)
             os.system("mv ./access_logs/access_log ./access_logs/access_log_%s" % inst.ip_address)

def generate_traffic_ELB():
 cmd = "./generateTraffic.sh &" 
 os.system(cmd)

def check_myInstances_Access_Logs():
 if len(myInstances) == 0:
     print('No instances in Colums Autoscale group Please ensure you have instances first')
 else:
     cmd = "ssh -t -o StrictHostKeyChecking=no -i " + key + " " + "ec2-user@"
     for inst in myInstances:
         print("Connecting to instance :  %s to check the apache access_log file........." % inst.id)
         run_command(cmd + inst.ip_address + " 'sudo cat /var/log/httpd/access_log' ")
         time.sleep(10)

def create_new_scaling_policy():
 autoscale_conn = boto.ec2.autoscale.connect_to_region('eu-west-1') 
 print(autoscale_conn)
 # lc = autoscale_conn.get_all_launch_configurations(names=['cFoskin_lc'])
 # print(lc)
 # myLc = lc[0]
 # print(myLc)
 asGroups = autoscale_conn.get_all_groups(names=['cFoskin_aGroup'])
 print(asGroups)
 myASGroup = asGroups[0]
 print(myASGroup)
 myTag = myASGroup.tags[0]
 print(myTag)
 scale_up_policy = ScalingPolicy(name='Scale up policy', adjustment_type='ChangeInCapacity', as_name='cFoskin_aGroup', scaling_adjustment=1, cooldown=180)
 autoscale_conn.create_scaling_policy(scale_up_policy)
 scale_down_policy = ScalingPolicy(name='Scale down policy', adjustment_type='ChangeInCapacity', as_name='cFoskin_aGroup', scaling_adjustment=1, cooldown=180)
 autoscale_conn.create_scaling_policy(scale_down_policy)

def set_up_cloudwatch_alarm():
 sns_conn = boto.sns.connect_to_region('eu-west-1')
 topics = sns_conn.get_all_topics()
 topic = topics[u'ListTopicsResponse']['ListTopicsResult']['Topics'][0]['TopicArn']
 cloudwatch_conn = boto.ec2.cloudwatch.connect_to_region('eu-west-1')
 alarm_name = 'columCpuMetricAlarm'

 

 elb_conn = boto.ec2.elb.connect_to_region('eu-west-1')
 elb = elb_conn.get_all_load_balancers(load_balancer_names='cFoskin-elb')[0]
 anInstance = myLb.instances[0]

 metric = cloudwatch_conn.list_metrics(dimensions={'InstanceId'::anInstance.id}, metric_name="CPUUtilization")[0]
 alarm = metric.create_alarm(name=alarm_name, comparison='>', threshold=60, period=300, evaluation_periods=1, statistic= 'Average', alarm_actions=[topic])
 
 policyResults = autoscale_conn.get_all_policies(as_group='cFoskin_aGroup', policy_names=[scale_up_policy])
 scale_up_policy = policyResults[0]

 alarm_actions = []
 alarm_actions.append(scale_up_policy.policy_arn)
 cloudwatch_conn.create_alarm(alarm)