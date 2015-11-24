#colum foskin 20062042
#!/usr/bin/python3
import boto.ec2.autoscale
from boto.ec2.autoscale import ScalingPolicy
from boto.sns import connect_to_region
from boto.ec2.cloudwatch import connect_to_region
from boto.ec2.elb import ELBConnection
from boto.ec2.cloudwatch import MetricAlarm
scale_up_policy = None
scale_down_policy = None
autoscale_conn = None
cloudwatch_conn = None
alarm_dimensions = None
alarm_tag = 'cFoskin_'


def open_autoscale_conn():
 global autoscale_conn
 autoscale_conn = boto.ec2.autoscale.connect_to_region('eu-west-1')  
 # asGroups = autoscale_conn.get_all_groups(names=['cFoskin_aGroup'])
 # myASGroup = asGroups[0]
 
def create_scale_up_policy():
 name = input('Enter The Name of Your new policy.. \n\n ')
 global scale_up_policy
 scale_up_policy = ScalingPolicy(name=name, adjustment_type='ChangeInCapacity', as_name='cFoskin_aGroup', scaling_adjustment=1, cooldown=180)
 autoscale_conn.create_scaling_policy(scale_up_policy)
 policyResults = autoscale_conn.get_all_policies(as_group='cFoskin_aGroup', policy_names=[scale_up_policy])
 scale_up_policy = policyResults[0]#Refresh to get Amazon Resource Name (ARN) of policy
 print('The policy : %s is now created....\n' % name)
 return bool(1)

def create_scale_downPolicy():
 name = input('Enter The Name of Your new policy.. \n\n ')
 global scale_down_policy
 scale_down_policy = ScalingPolicy(name=name, adjustment_type='ChangeInCapacity', as_name='cFoskin_aGroup', scaling_adjustment=-1, cooldown=180)
 autoscale_conn.create_scaling_policy(scale_down_policy) 
 policyResults = autoscale_conn.get_all_policies(as_group='cFoskin_aGroup', policy_names=[scale_down_policy])
 scale_down_policy = policyResults[0]#Refresh to get Amazon Resource Name (ARN) of policy
 print('The policy : %s is now created....\n' % name)
 return bool(1)

def create_scale_up_alarm():
 name = input('Enter The Name of Your new Alarm.. \n\n ')
 scale_up_alarm_name= alarm_tag + name
 scale_up_alarm = MetricAlarm(name=scale_up_alarm_name, namespace='AWS/EC2',metric='CPUUtilization', statistic='Average',comparison='>', threshold='70', period='60', evaluation_periods=2,alarm_actions=[scale_up_policy.policy_arn],dimensions=alarm_dimensions)
 cloudwatch_conn.create_alarm(scale_up_alarm)
 print('The cloud watch alarm : %s is now created....\n' % scale_up_alarm_name)

def create_scale_down_alarm():
 name = input('Enter The Name of Your new Alarm.. \n\n ') 
 scale_down_alarm_name = alarm_tag + name
 scale_down_alarm = MetricAlarm(name=scale_down_alarm_name, namespace='AWS/EC2',metric='CPUUtilization', statistic='Average',comparison='>', threshold='70', period='60', evaluation_periods=2,alarm_actions=[scale_down_policy.policy_arn],dimensions=alarm_dimensions)
 cloudwatch_conn.create_alarm(scale_down_alarm)
 print('The cloud watch alarm : %s is now created....\n' % scale_down_alarm_name)

def set_up_cloud_watch():
 global cloudwatch_conn
 cloudwatch_conn = boto.ec2.cloudwatch.connect_to_region('eu-west-1')
 global alarm_dimensions
 alarm_dimensions = {"AutoScalingGroupName": 'cFoskin_aGroup'}
 return bool(1)
    