#!/usr/bin/env python3
#Author: Xuejian Sundvall
#Date: October 20th, 2025

import subprocess
import pathlib

#Prints a header informing the user what program this is
def print_header():
    print("**************************")
    print("**** Shortcut Creator ****")
    print("**************************");

#Prints the options this program offers
def print_options():
    print("Enter Selection:")
    print()
    print("\t1 - Create a shortcut in your home directory")
    print("\t2 - Remove a shortcut from your home directory")
    print("\t3 - Run shortcut report")
    print()

#Runs a bash command and returns the stdout as a string
def run(command):
    return subprocess.run(command, shell=True, capture_output=True, text=True).stdout

#Looks for a file with the given filename in the entire file system
#If multiple files with the same name is found, prompts the user to choose one
#Returns the full path of the desired file
def find_file(filename):
    files = run("sudo find / -name '" + filename + "' 2> /dev/null").strip()
    if files == '':
        print("No such file: " + filename)
        return

    files = files.split("\n")
    if len(files) == 1:
        print("Found exactly one file");
        return files[0]
    else:
        print("Multiple files were found")
        for index, file in enumerate(files):
            print("\t" + str(index + 1) + " - " + file)
        target_index = input("Please select the file you wish to create a shortcut for (1-" + str(len(files)) + "):")
        while not target_index.isdigit() or int(target_index) not in range(1, len(files) + 1):
            print("Invalid input, please try again")
            target_index = input("Please select the file you wish to create a shortcut for (1-" + str(len(files)) + "): ")
        return files[int(target_index) - 1]

#Prompts the user to select a operation to run
def get_input():
    user_input = 0
    print_options()
    user_input = input("Please enter a number (1-3) or \"Q/q\" to quit the program: ")
    while user_input not in ('1', '2', '3', 'Q', 'q'):
        print("Invalid input, please try again")
        print_options()
        user_input = input("Please enter a number (1-3) or \"Q/q\" to quit the program: ")
    return user_input

#Creates a symlink in the home directory with the same name as the target file
def create_symlink(filename):
    if filename is None:
        return
    print("Are you sure you want to create a symlink for " + filename + "?")
    proceed = input("Select (Y/y) to continue: ")
    if proceed in ('Y', 'y'):
        run("ln -s " + filename + ' ' + str(pathlib.Path.home()) + '/' + filename.split("/")[-1])
        print("Symlink created")
    else:
        print("Symlink creation aborted")

#Deletes the symlink with the given filename in the home directory if it exists
def delete_symlink(filename):
    full_path = str(pathlib.Path.home()) + '/' + filename
    if run("ls " + full_path) != '':
        run("rm " + full_path);
        print(filename + " symlink has been deleted")
    else:
        print("File not found: " + filename)

#Prints a report showing the current directory, and a list of symlink
#in the home directory along with their paths
def print_report():
    print("Current Directory: " + run("pwd"))
    output = run("ls -l " + str(pathlib.Path.home()) + " | grep '^l'").strip()

    if output == '':
        print("No symlinks found")
    else:
        lines = output.split("\n")
        print("The number of links is " + str(len(lines)))
        if len(lines) != 0:
            print("Symbolic Links\t\t\tTarget Path")
        for line in lines:
            tokens = line.split()
            symlink = tokens[8]
            target_path = tokens[10]
            print(symlink + "\t\t\t" + target_path)

def main():
    subprocess.run(["clear"])
    print_header()
    user_input = get_input()

    while user_input not in ('Q', 'q'):
        print()
        if user_input == '1':
            create_symlink(find_file(input("Enter file name: ")))
        elif user_input == '2':
            delete_symlink(input("Enter the symlink you wish to delete: "))
        else:
            print_report()
        print()
        user_input = get_input()

if __name__ == "__main__":
    main()
