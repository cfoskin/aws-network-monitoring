#colum foskin 20062042
#!/usr/bin/python3
# a menu for the user
from termcolor import colored
from monitor_instances import *
from manage_autoscale import *
import sys
connection = None

def mainOptions():
 choice = None
 while choice != '0':
     print(colored("\n\n Welcome to the Main Menu  ", 'green',attrs=['reverse', 'blink']))
     print('=============                 Main Menu              =============')
     print('==================================================================')
     print('|  1: Retrieve and View all instances in my Autoscale group        |')
     print('|  2: Copy the apache access logs to a local direcory              |')
     print('|  3: Generate traffic to ELB                                      |')
     print('|  4: Check the access logs for instances in the ELB               |')
     print('|  5: Manage Autoscale Group                                       |')
     print(colored('|  0: EXIT                                                        |', 'red'))
     print('==================================================================')
     choice = input('which task do you want to perform? \n\n ')
     if choice == '1': listMyInstances(connection)
     if choice == '2': copy_access_logs_to_local()
     if choice == '3': generate_traffic_ELB()
     if choice == '4': check_myInstances_Access_Logs() 
     if choice == '5': autoscaleOptions() 
     if choice == '0': sys.exit(0)  

def autoscaleOptions():
 choice = None
 while choice != '0':
     print(colored("\n\n Welcome To The Autoscale Menu ", 'green',attrs=['reverse', 'blink']))
     print('==================================================================')
     print('|  1: Create new policies for my autoscale group                   |')
     print('|  2: Create new cloud watch alarm                                 |')
     print(colored('|  0: Return to Main Menu                                                       |', 'red'))
     print('==================================================================')
     choice = input('which task do you want to perform? \n\n ')
     if choice == '1': create_new_scaling_policies()
     if choice == '2': create_cloudwatch_alarm()
     if choice == '0': mainOptions()   

def main():
 global connection
 connection = connect()
 mainOptions()

if __name__ == '__main__':
  main()
