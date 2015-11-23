#colum foskin 20062042
#!/usr/bin/python3
# a menu for the user
from termcolor import colored
from monitor import *
import sys
connection = None

def options():
 choice = None
 while choice != '0':
     print(colored("\n\n Welcome  ", 'green',attrs=['reverse', 'blink']))
     print('=============                 Main Menu              =============')
     print('==================================================================')
     print('|  1: Retrieve and View all instances in my Autoscale group        |')
     print('|  2: Copy the apache access logs to a local direcory                         |')
     #print('|  3: Copy the apache access logs to a local direcory                     |')
     # print('|  4: Copy Nginx webserver script using SCP                       |')
     # print('|  5: Change webserver script permissions                         |')
     # print('|  6: Install Python 3 on instance                                |')
     # print('|  7: Run script to check if Nginx is running and start if not    |')
     # print('|  8: Stop Instance                                               |')
     # print('|  9: Terminate Instance                                          |')
     # print(colored('|  t: Test nginx is running correctly using lynx                  |','green'))
     # print(colored('|  l: View  Nginx acces log file                                  |','green'))
     # print(colored('|  e: View local ec2 error log                                    |','green'))
     print(colored('|  0: EXIT                                                        |', 'red'))
     print('==================================================================')
     choice = input('which task do you want to perform? \n\n ')
     if choice == '1': listMyInstances(connection)
     if choice == '2': copy_access_logs_to_local()
    # if choice == '3': 
     # if choice == '5': make_executable() 
     # if choice == '6': install_python() 
     # if choice == '7': run_webserver_script()
     # if choice == '8': stop_instance()
     # if choice == '9': terminate_instance()
     # if choice == 't': test()
     # if choice == 'l': nginx_log()
     # if choice == 'e': view_error_log()
     if choice == '0': sys.exit(0)    

def main():
 global connection
 connection = connect()
 options()
 
if __name__ == '__main__':
  main()
