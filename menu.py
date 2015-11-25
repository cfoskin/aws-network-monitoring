#colum foskin 20062042
#!/usr/bin/python3
#A set of menus for the user
from termcolor import colored
from utility import *
from manage_autoscale import *
import sys
connection = None
scaling_up_policy_created = bool(0)
scaling_up_alarm_created = bool(0)
scaling_down_policy_created = bool(0)
scaling_down_alarm_created = bool(0)

#main menu
def mainOptions():
 getAllMyInstances(connection)#gather my instances and store them in an array
 choice = None
 while choice != '0':
     print(colored("\n\n Welcome to the Main Menu  ", 'green',attrs=['reverse', 'blink']))
     print('=============                 Main Menu              =============')
     print('==================================================================')
     print('|  1: View all instances in my Autoscale group                     |')
     print('|  2: Manage Autoscale Group                                       |')
     print('|  3: View options for Elb and Instance Access log management      |')              
     print(colored('|  0: EXIT                                                        |', 'red'))
     print('==================================================================')
     choice = input('which task do you want to perform? \n\n ')
     if choice == '1': listMyInstances()
     if choice == '2': autoscaleOptions()
     if choice == '3': utility_options()
     if choice == '0': sys.exit(0)  

#utility menu
def utility_options():
 getAllMyInstances(connection)#gather my instances and store them in an array
 choice = None
 while choice != '0':
     print(colored("\n\n Welcome To The Utility Menu ", 'green',attrs=['reverse', 'blink']))
     print('==================================================================')
     print('|  1: Generate traffic to ELB                                      |')
     print('|  2: View the access logs for the instances                       |')
     print('|  3: Copy the apache access logs to a local direcory              |')    
     print(colored('|  0: Return to Main Menu                                                       |', 'red'))
     print('==================================================================')
     choice = input('which task do you want to perform? \n\n ')
     if choice == '1': generate_traffic_ELB()
     if choice == '2': check_myInstances_Access_Logs()
     if choice == '3': copy_access_logs_to_local()
     if choice == '0': mainOptions()   

#autoscaling menu
def autoscaleOptions():
 choice = None
 while choice != '0':
     print(colored("\n\n Welcome To The Autoscale Menu ", 'green',attrs=['reverse', 'blink']))
     print('==================================================================')
     print('|  1: Create new policies for my autoscale group                   |')
     print('|  2: Create new cloud watch alarm                                 |')
     print(colored('|  3: Trigger an autoscaling scale up event based on new policy    |', 'green'))
     print(colored('|  0: Return to Main Menu                                                       |', 'red'))
     print('==================================================================')
     choice = input('which task do you want to perform? \n\n ')
     if choice == '1': policy_Options()
     if choice == '2': cloud_watch_options()
     if choice == '3': 
         if scaling_up_alarm_created:
             trigger_autoscaling_event()  
         else: print(colored('Please create a scaling up alarm and policy first', 'red')) 
     if choice == '0': mainOptions()   

#policy menu
def policy_Options():
 choice = None
 open_autoscale_conn()
 while choice != '0':
     print('==================================================================')
     print(colored('|  1: Create a scaling up autoscale policy                         |', 'green'))
     print(colored('|  2: Create a scaling down autoscale policy                       |', 'green'))
     print(colored('|  0: Return to Autoscale menu                          |', 'red'))
     print('==================================================================')
     choice = input('which task do you want to perform? \n\n ')
     if choice == '1':
         global scaling_up_policy_created
         scaling_up_policy_created = create_scale_up_policy()
     if choice == '2': 
         global scaling_down_policy_created
         scaling_down_policy_created = create_scale_downPolicy()
     if choice == '0': autoscaleOptions()   

#cloud watch menu
def cloud_watch_options():
 set_up_cloud_watch()
 choice = None
 while choice != '0':
     print('==================================================================')
     print(colored('|  1: Create a scaling up cloud watch alarm                       |', 'green'))
     print(colored('|  2: Create a scaling down cloud watch alarm                     |', 'green'))
     print(colored('|  0: Return to Autoscale menu                         |', 'red'))
     print('==================================================================')
     choice = input('which task do you want to perform? \n\n ')
     if choice == '1': 
         if scaling_up_policy_created:
             global scaling_up_alarm_created
             scaling_up_alarm_created = create_scale_up_alarm()
         else: print(colored('Please create a scale up policy first', 'red'))
     if choice == '2': 
         if scaling_down_policy_created:
             global scaling_down_alarm_created
             scaling_down_alarm_created = create_scale_down_alarm()
         else: print(colored('Please create a scale down policy first', 'red'))
     if choice == '0': autoscaleOptions()   

def main():
 global connection
 connection = connect()
 mainOptions()

if __name__ == '__main__':
  main()
