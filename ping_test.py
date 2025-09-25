#!/usr/bin/env python3
#Xuejian Sundvall
#September 10th, 2025
import subprocess

#Displays the options for this tool
def display_options():
    print("1. Display the Default Gateway")
    print("2. Test Local Connectivity")
    print("3. Test Remote Connectivity")
    print("4. Test DNS Resolution")
    print("5. Exit/Quit the Script")

#Returns the default gateway
def get_default_gateway():
    result = subprocess.run("ip r", capture_output=True, shell=True).stdout.decode()
    return result.split(" ")[2]

#Prints the default gateway to the screen
def display_default_gateway():
    print(get_default_gateway())

#Displays a success or failure messagee based on returncode from the output
#of subprocess.run
def display_output_message(result):
    if result.returncode == 0:
        print("SUCCESS")
    else:
        print("FAILURE")

#Tests local connectivity by sending 4 pings to the default gateway with a
#5 second timeout
def test_local_connectivity():
    default_gateway = get_default_gateway()
    print("pinging " + default_gateway + "...")
    result = subprocess.run("ping " + default_gateway + " -c 4 -w 5", capture_output=True, shell=True)
    display_output_message(result)

#Tests remote connectivity by sending 4 pings to RIT's DNS server with a
#5 second timeout
def test_remote_connectivity():
    print("pinging 129.21.3.17...")
    result = subprocess.run("ping 129.21.3.17 -c 4 -w 5", capture_output=True, shell=True)
    display_output_message(result)

#Tests DNS resolution using nslookup for www.google.com using RIT's DNS server
def test_dns_resolution():
    print("Checking DNS Resolution for www.google.com...")
    result = subprocess.run("nslookup www.google.com 129.21.3.17", capture_output=True, shell=True)
    display_output_message(result)

#Gets user input and handles error checking
def handle_input():
        is_valid = False
        option = -1
        while not is_valid:
            option = input("Enter Option: ")
            if not is_number(option):
                print("INVALID INPUT: Not a Number")
                is_valid = False
                continue
            option = int(option)
            if option > 5 or option < 1:
                print("INVALID INPUT: Value Must be Between 1 and 5 inclusive")
                is_valid = False
            else:
                is_valid = True
        return option

#returns true if the given value is a numeric string
def is_number(value):
    if value[0] == '-':
        return value[1:].isdigit()
    return value.isdigit()

if __name__ == "__main__":
    subprocess.run("clear")
    display_options()
    option = handle_input()
    while option != 5:
        if option == 1:
            display_default_gateway()
        elif option == 2:
            test_local_connectivity()
        elif option == 3:
            test_remote_connectivity()
        elif option == 4:
            test_dns_resolution()
        print("----------------------------------------")
        display_options()
        option = handle_input()

