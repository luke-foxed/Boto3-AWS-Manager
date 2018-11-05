#!/usr/bin/python3


# NOTE: Please run this script using python3 when in SSH

import subprocess


def menu():
    print("\nWelcome!\n")
    print("1) Check NGINX Status")
    print("2) Check resources")
    print("3) Check MQSQL")

    option = input("\nPlease select an option: ")

    if option == '1':
        print('Checking NGINX...\n')
        check_web()
        menu()
    elif option == '2':
        print('Checking resources...\n')
        check_resources()
        menu()
    elif option == '3':
        print('Checking MYSQL...\n')
        check_db()
        menu()
    else:
        print('\nPlease enter a valid option')
        menu()
    return


def check_web():
    try:
        p = subprocess.run('ps -A | grep nginx', shell=True)  # list running nginx instances
        if (p.returncode == 0):
            print(p)
        else:
            print("No server running!")
            subprocess.run('sudo amazon-linux-extras install nginx1.12', shell=True)
            subprocess.run('sudo service nginx start', shell=True)  # if server is not running, start one

    except Exception as error:
        print(error)


def check_resources():
    subprocess.run("sudo yum -y install sysstat", shell=True)
    execute = subprocess.Popen('vmstat')
    print("\n Resources Table \n ---------- \n")
    print(execute)
    processes = subprocess.run('ps -eo pcpu,pmem,args | sort -k 1 -r | less',  # list every process and server, with usage
                               shell=True)  # source: http://go2linux.garron.me/vmstat-cpu-memory-monitor-linux-fix-low-mem/
    print("\n Processes Table \n ---------- \n")
    print(processes)


def check_db():
    try:
        db = subprocess.run('mysqladmin status', shell=True)
        if (db.returncode == 0):
            print("\n + db")
        else:
            print("No database running")

    except Exception as error:
        print(error)


if __name__ == '__main__':
    menu()
