#colum foskin 20062042
#!/usr/bin/python3
# This python module provides functionality for the options in the autoscaling menus and sub menus
# in the menu module. It provides functionality for creating autoscaling alarms and policies while also allows
# the user to test the scaling policies.

import boto.ec2.autoscale
from boto.ec2.autoscale import ScalingPolicy
from boto.sns import connect_to_region
from boto.ec2.cloudwatch import connect_to_region
from boto.ec2.cloudwatch import MetricAlarm
from utility import *
scale_up_policy = None
scale_down_policy = None
autoscale_conn = None
cloudwatch_conn = None
alarm_dimensions = None
alarm_tag = 'cFoskin_'

#open autoscale connection
def open_autoscale_conn():
 global autoscale_conn
 autoscale_conn = boto.ec2.autoscale.connect_to_region('eu-west-1')  

#allows the user to create a policy to scale up
def create_scale_up_policy():
 name = input('Enter The Name of Your new policy.. \n\n ')
 global scale_up_policy
 scale_up_policy = ScalingPolicy(name=name, adjustment_type='ChangeInCapacity', as_name='cFoskin_aGroup', scaling_adjustment=1, cooldown=180)
 autoscale_conn.create_scaling_policy(scale_up_policy)
 policyResults = autoscale_conn.get_all_policies(as_group='cFoskin_aGroup', policy_names=[scale_up_policy])
 scale_up_policy = policyResults[0]#Refresh to get Amazon Resource Name (ARN) of policy
 print('The policy : %s is now created....\n' % name)
 print('Please create the corresponding alarm')
 return bool(1)

#allows the user to create a policy to scale down
def create_scale_downPolicy():
 name = input('Enter The Name of Your new policy.. \n\n ')
 global scale_down_policy
 scale_down_policy = ScalingPolicy(name=name, adjustment_type='ChangeInCapacity', as_name='cFoskin_aGroup', scaling_adjustment=-1, cooldown=180)
 autoscale_conn.create_scaling_policy(scale_down_policy) 
 policyResults = autoscale_conn.get_all_policies(as_group='cFoskin_aGroup', policy_names=[scale_down_policy])
 scale_down_policy = policyResults[0]#Refresh to get Amazon Resource Name (ARN) of policy
 print('The policy : %s is now created....\n' % name)
 return bool(1)

#allows the user to create an alarm for the scale up policy 
def create_scale_up_alarm():
 name = input('Enter The Name of Your new Alarm.. \n\n ')
 scale_up_alarm_name= alarm_tag + name
 scale_up_alarm = MetricAlarm(name=scale_up_alarm_name, namespace='AWS/EC2',metric='CPUUtilization', statistic='Average',comparison='>', threshold='40', period='60', evaluation_periods=2,alarm_actions=[scale_up_policy.policy_arn],dimensions=alarm_dimensions)
 cloudwatch_conn.create_alarm(scale_up_alarm)
 print('The cloud watch alarm : %s is now created....\n' % scale_up_alarm_name)
 return bool(1)

#allows the user to create an alarm for the scale down policy 
def create_scale_down_alarm():
 name = input('Enter The Name of Your new Alarm.. \n\n ') 
 scale_down_alarm_name = alarm_tag + name
 scale_down_alarm = MetricAlarm(name=scale_down_alarm_name, namespace='AWS/EC2',metric='CPUUtilization', statistic='Average',comparison='<', threshold='35', period='60', evaluation_periods=2,alarm_actions=[scale_down_policy.policy_arn],dimensions=alarm_dimensions)
 cloudwatch_conn.create_alarm(scale_down_alarm)
 print('The cloud watch alarm : %s is now created....\n' % scale_down_alarm_name)
 return bool(1)

#retrieves an instance and copys up the cpu100.sh using scp, make it executable and run it. 
#user can press ctr+c at any time to exit the process and it will return to the menu.
def trigger_autoscaling_event():
 inst = myInstances[1]
 ip_address = inst.ip_address
 cmd_scp = "scp -o StrictHostKeyChecking=no -i" + key + " cpu100.sh " + "ec2-user@"+ip_address +":."  
 if run_command(cmd_scp):
     print('Script copied up. Making executable....')
     cmd_exec = "ssh -t -i " + key + " " + "ec2-user@"+ip_address +" 'chmod 700 cpu100.sh'"
     if run_command(cmd_exec):
         cmd_run = "ssh -t -i " + key + " " + "ec2-user@"+ip_address +" './cpu100.sh'"
         print('Process starting on instance: %s .... \n' % inst)
         print('Press ctrl + c to kill this process and return to the main menu to view any new instances')
         if run_command(cmd_run):
             print('Please return to main menu now to view your instances\n')
             print('Any new instances spun up will scale down automatically when allowed the time to do so\n')
         else: print('Exiting ..... ')  
     else: print('error making executable... Please retry')
 else: print('error with scp... Please retry')
       
#open cloud watch connection and set dimensions
def set_up_cloud_watch():
 global cloudwatch_conn
 cloudwatch_conn = boto.ec2.cloudwatch.connect_to_region('eu-west-1')
 global alarm_dimensions
 alarm_dimensions = {"AutoScalingGroupName": 'cFoskin_aGroup'}
 return bool(1)
    