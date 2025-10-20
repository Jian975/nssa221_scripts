#!/usr/bin/python

#Author: Xuejian Sundvall
#Date: October 11th, 2025

import subprocess;
from datetime import date
import ipaddress
import sys

#custom stdout that writes to both the terminal and the log file
class DualStdOut:
    def __init__(self, hostname):
        self.terminal = sys.stdout
        self.log = open(hostname + "_system_report.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

#update stdout to point to both terminal and log file
sys.stdout = DualStdOut(subprocess.run("hostname", text=True, shell=True, capture_output=True).stdout.split(".")[0])

#prints the device hostname and domain
def print_device_information():
    output = subprocess.run("hostname", text=True, shell=True, capture_output=True).stdout.split(".")
    hostname = output[0]
    domain = output[1]
    print("Device Information")
    print("Hostname:\t\t\t", hostname)
    print("Domain:\t\t\t\t", domain)

#returns the non-loopback IP address of this host
def get_ip():
    output = subprocess.run("ip addr show scope global", shell=True, capture_output=True, text=True).stdout
    lines = output.split("\n")
    for line in lines:
        if line.strip().startswith("inet "):
            ip = line.split("/")[0]
            return ip[9:]

#returns the subnet mask associated with the non-loopback IP address of this host
def get_network_mask():
    output = subprocess.run("ip addr show scope global", shell=True, capture_output=True, text=True).stdout
    lines = output.split("\n")
    for line in lines:
        if line.strip().startswith("inet "):
            cidr = line.split("/")[1][:2]
            return ipaddress.IPv4Network("192.168.1.0/" + cidr, strict=False).netmask

#Prints the two DNS servers this host uses
def print_dns():
    output = subprocess.run("cat /etc/resolv.conf", shell=True, text=True, capture_output=True).stdout
    lines = output.split("\n")
    i = 0;
    for line in lines:
        if line.strip().startswith("nameserver"):
            print("DNS" + str(i) + ":\t\t\t\t", line.split(" ")[1])
            i = i+1

#Prints the default gateway of this host
def get_default_gateway():
    output = subprocess.run("ip route show default", shell=True, capture_output=True, text=True).stdout
    return output.split(" ")[2]

#Prints the IP address, subnet mask, default gateway, and DNS servers of this host
def print_network_information():
    print("Network Information")
    ip = get_ip()
    default_gateway = get_default_gateway()
    mask = get_network_mask()
    print("IP Address:\t\t\t", ip)
    print("Gateway:\t\t\t", default_gateway)
    print("Network Mask:\t\t\t", mask)
    print_dns()
    print()

#Prints the OS name, OS version, and kernel version of this host
def print_os_information():
    print("Operating System Information")
    output = subprocess.run("cat /etc/*release", shell=True, capture_output=True, text=True).stdout
    lines = output.split("\n")
    for line in lines:
        if line.strip().startswith("PRETTY_NAME"):
            print("Operating System:\t\t", line.split("=")[1][1:-1])
        if line.strip().startswith("VERSION_ID"):
            print("OS Version:\t\t\t", line.split("=")[1][1:-1])
    print("Kernel Version:\t\t\t", subprocess.run("uname -r", shell=True, capture_output=True, text=True).stdout)

#Prints a title in the form "System Report - <today's date>"
def print_title():
    today_formatted = date.today().strftime("%B %d, %Y")
    print()
    print("                  System Report - ", today_formatted)
    print()

#Prints the CPU model, number of cores, and number of processors
def print_processor_information():
    print("Processor Information")
    output = subprocess.run("cat /proc/cpuinfo", shell=True, capture_output=True, text=True).stdout
    for line in output.split("\n"):
        if line.strip().startswith("model name"):
            print("CPU Model:\t\t\t", line.split(":")[1].strip())
        if line.strip().startswith("cpu cores"):
            print("Number of cores:\t\t", line.split(":")[1].strip())
    print("Number of processors:\t\t", subprocess.run("nproc", shell=True, capture_output=True, text=True).stdout)

#Prints the total, free, and used amounts on the disk
def print_storage_information():
    print("Storage Information")
    line = subprocess.run("df -BG /", shell=True, capture_output=True, text=True).stdout.split("\n")[1]
    print("System Drive Total:\t\t", line.split()[1])
    print("System Drive Used:\t\t", line.split()[2])
    print("System Drive Free:\t\t", line.split()[3])
    print()

#Prints the total amount of RAM and the amount of RAM available
def print_memory_information():
    print("Memory Information")
    line = subprocess.run("free --si -h", shell=True, capture_output=True, text=True).stdout.split("\n")[1]
    print("Total RAM:\t\t\t", line.split()[1])
    print("Available RAM:\t\t\t", line.split()[3])
    print()
    
def main():
    subprocess.run("clear", shell=True)
    print_title()
    print_device_information()
    print_network_information()
    print_os_information()
    print_storage_information()
    print_processor_information()
    print_memory_information()
    
if __name__ == "__main__":
    main()
