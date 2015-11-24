import boto.ec2.autoscale
from boto.ec2.autoscale import ScalingPolicy
from boto.sns import connect_to_region
from boto.ec2.cloudwatch import connect_to_region
from boto.ec2.elb import ELBConnection
from boto.ec2.cloudwatch import MetricAlarm
scale_up_policy = None
scale_down_policy = None

def create_new_scaling_policies():
 autoscale_conn = boto.ec2.autoscale.connect_to_region('eu-west-1') 
 # asGroups = autoscale_conn.get_all_groups(names=['cFoskin_aGroup'])
 # myASGroup = asGroups[0]
 global scale_up_policy
 scale_up_policy = ScalingPolicy(name='Generated Scale up policy', adjustment_type='ChangeInCapacity', as_name='cFoskin_aGroup', scaling_adjustment=1, cooldown=180)
 autoscale_conn.create_scaling_policy(scale_up_policy)
 global scale_down_policy
 scale_down_policy = ScalingPolicy(name='Generated Scale down policy', adjustment_type='ChangeInCapacity', as_name='cFoskin_aGroup', scaling_adjustment=-1, cooldown=180)
 autoscale_conn.create_scaling_policy(scale_down_policy)
 policyResults = autoscale_conn.get_all_policies(as_group='cFoskin_aGroup', policy_names=[scale_up_policy])
 scale_up_policy = policyResults[0]#Refresh to get Amazon Resource Name (ARN) of each policy
 policyResults = autoscale_conn.get_all_policies(as_group='cFoskin_aGroup', policy_names=[scale_down_policy])
 scale_down_policy = policyResults[0]#Refresh to get Amazon Resource Name (ARN) of each policy

def create_cloudwatch_alarm():
 if scale_up_policy == None:
     print("You need to create a scaling policy to create a cloudwatch alarm")
 else:    
     cloudwatch_conn = boto.ec2.cloudwatch.connect_to_region('eu-west-1')
     sns_conn = boto.sns.connect_to_region('eu-west-1')
     scale_up_alarm_name = 'Generated_scale_up_cFoskin_CpuMetricAlarm'
     scale_down_alarm_name = 'Generated_scale_down_cFoskin_CpuMetricAlarm'
     alarm_dimensions = {"AutoScalingGroupName": 'cFoskin_aGroup'}
     scale_up_alarm = MetricAlarm(name=scale_up_alarm_name, namespace='AWS/EC2',metric='CPUUtilization', statistic='Average',comparison='>', threshold='70', period='60', evaluation_periods=2,alarm_actions=[scale_up_policy.policy_arn],dimensions=alarm_dimensions)
     scale_down_alarm = MetricAlarm(name=scale_down_alarm_name, namespace='AWS/EC2',metric='CPUUtilization', statistic='Average',comparison='>', threshold='70', period='60', evaluation_periods=2,alarm_actions=[scale_down_policy.policy_arn],dimensions=alarm_dimensions)
     cloudwatch_conn.create_alarm(scale_up_alarm)
     cloudwatch_conn.create_alarm(scale_down_alarm)
