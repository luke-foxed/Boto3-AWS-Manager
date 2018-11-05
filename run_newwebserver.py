#!/usr/bin/python3

# NOTE: Some of the code shown below has been sourced from the lab material

import boto3
import subprocess
import time
import webbrowser


def menu():
    print("\nWelcome!\n")
    print("1) Create an instance")
    print("2) Add tag to instance")
    print("3) Get EC2 DNS names")
    print("4) Create a bucket")
    print("5) Add to a bucket")
    print("6) List buckets")
    print("7) Delete an instance")
    print("8) Delete a bucket")
    print("9) Delete bucket contents")
    print("10) Move bucket image to nginx")
    print("\n-------------------\n")
    print("11) SSH into instance")

    option = input("\nPlease select an option: ")

    if option == '1':
        print('Creating an instance...\n')
        create_instance("", "")  # passed with empty arguemnts so that input will be used by default
        menu()
    elif option == '2':
        print('Setting tag...\n')
        create_tag()
        menu()
    elif option == '3':
        print('Getting EC2 DNS names...\n')
        list_ec2_dns()
        menu()
    elif option == '4':
        print('Creating a bucket...\n')
        create_bucket("")
        menu()
    elif option == '5':
        put_bucket()
        menu()
        print('Adding to bucket...\n')
    elif option == '6':
        print('List buckets...\n')
        list_buckets()
        menu()
    elif option == '7':
        print('Deleting an instance...\n')
        terminate_instance("")
        menu()
    elif option == '8':
        print('Deleting a bucket...\n')
        delete_bucket("")
        menu()
    elif option == '9':
        print('Deleting contents...\n')
        delete_contents()
        menu()
    elif option == '10':
        print('Moving image...\n')
        move_html()
        menu()
    elif option == '11':
        print('SSH into instance...\n')
        ssh_instance()
        menu()
    else:
        print('\nPlease enter a valid option')
        menu()
    return


def create_instance(key, security):  # parameters used for testing class
    ec2 = boto3.resource('ec2')
    if(key == ""):  # ignore arguements and take user input
        key = input("Please enter the name of your key: ")
    if(security == ""):
        security = input("Please enter the name of your security group: ")
    try:
        instance = ec2.create_instances(
            ImageId='ami-0bdb1d6c15a40392c',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName=key,
            SecurityGroups=[security],
            UserData='''#!/bin/bash
                    sudo yum update -y
                    pip3 install boto3
                    sudo yum install python3 -y
                    sudo amazon-linux-extras install nginx1.12 -y
                    sudo service nginx start
                    touch /home/ec2-user/testfile''',  # to check all ok
        )
        print("\nCreated instance!")
        print("Waiting 15 seconds for instance to start up\n")
        for i in range(15, 0, -1):
            time.sleep(1)  # To allow services to start and instance to begin
            print(i)
        instance[0].reload
        return instance[0]
    except Exception as error:
        print(error)


def create_tag():
    ec2 = boto3.resource('ec2')
    name = input("Please enter Image ID of instance you wish to tag: ")
    try:
        instance = ec2.Instance(name)
        instance.reload
        value = input("Please enter a value for the tag: ")
        name_tag = {'Key': 'Name', 'Value': value}
        instance.create_tags(Tags=[name_tag])
    except Exception as error:
        print(error)


def list_ec2_dns():
    ec2 = boto3.resource('ec2')
    counter = 1
    for instance in ec2.instances.all():
        # only return instances whos states are 'running'
        if instance.state["Name"] == "running":
            print(str(counter) + ") DNS Name: " + instance.public_dns_name +
                  " ||| Image ID: " + instance.instance_id + "\n")
            counter = counter + 1
    else:
        print("----")


def create_bucket(bucket_name):
    s3 = boto3.resource("s3")
    if(bucket_name == ""):
        bucket_name = input("Please enter a bucket name: ")
    try:
        response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-1'}, ACL=(
            "public-read"))  # set permissions for bucket so that contents are publically accessible
        print(response)
        return response
    except Exception as error:
        print(error)


def list_buckets():
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)
        print("\n---")
        try:
            for item in bucket.objects.all():
                print("\t%s" % item.key)
                print("\n---")
        except Exception as error:
            print(error)


def delete_bucket(name):
    s3 = boto3.resource('s3')
    if(name == ""):
        name = input("Please enter the name of the bucket you wish to delete: ")
    bucket = s3.Bucket(name)
    try:
        response = bucket.delete()
        print(response)
    except Exception as error:
        print(error)


def terminate_instance(image_id):
    ec2 = boto3.resource('ec2')
    if(image_id == ""):
        image_id = input("Please enter the image ID: ")
    instance1 = str(ec2.Instance(image_id))
    for instance in ec2.instances.all():
        print(instance1)
        if instance.instance_id in instance1:
            print("\nFound instance...terminating\n")
            response = instance.terminate()
            print(response)
        else:
            print("ERROR! Instance not found!")


def put_bucket():
    s3 = boto3.resource('s3')
    bucket_names = []
    for bucket in s3.buckets.all():
        bucket_names.append(bucket.name)
    bucket_name = input(
        "Please enter the bucket you would like to put your object into: ")
    if (bucket_name in bucket_names):
        object_name = input("Please enter name of your object: ")
        try:
            response = s3.Object(bucket_name, object_name).put(
                Body=open(object_name, 'rb'), ACL=("public-read"))
            print(response)
            print("Waiting for object to upload...")
            time.sleep(15)  # allowing time for object to be uploaded
            link = "https://s3-eu-west-1.amazonaws.com/" + bucket_name + "/" + object_name
            print("Image link: " + link)
            subprocess.run(
                "echo '<html lang='en'><head><meta charset='utf-8'><title>Bucket Image</title></head><body><h1>Image</h1><img src='"
                + link + "'></</body></html>' >  image.html",
                shell=True)  # echo html code with image url to new image.html
        except Exception as error:
            print(error)
    else:
        print("No bucket found!")


def delete_contents():
    s3 = boto3.resource('s3')
    name = input("Please enter the name of the bucket whos contents you wish to delete: ")
    bucket_names = []
    for bucket in s3.buckets.all():
        bucket_names.append(bucket.name)
    if (name in bucket_names):
        bucket = s3.Bucket(name)
        for key in bucket.objects.all():
            try:
                response = key.delete()
                print(response)
            except Exception as error:
                print(error)
    else:
        print("Bucket does not exist!")


def move_html():
    ec2 = boto3.resource('ec2')
    warning = input("Have made a bucket and placed an inside?(y/n)")
    if (warning == 'y'):
        dns_name = input("Please enter the public DNS of the instance: ")
        for instance in ec2.instances.all():
            if (instance.public_dns_name == dns_name):  # error handling to ensure instance exists
                try:
                    subprocess.run(
                        "scp -i Assignment1.pem image.html ec2-user@" + dns_name + ":",
                        shell=True)  # colon to specify the default location in the instance
                    print("\n Successfully copied image script to current instance!")
                    time.sleep(5)  # allow html file to copy
                    subprocess.run(
                        "ssh -t -o StrictHostKeyChecking=no -i Assignment1.pem ec2-user@" + dns_name +
                        " sudo mv image.html /usr/share/nginx/html",
                        shell=True)  # ssh into instance and move html to correct location
                    url = "http://" + dns_name + "/image.html"  # generate link for browser to open
                    webbrowser.open_new(url)  # open url with default browser
                except Exception as error:
                    print(error)
            else:
                print("No instance found matching this DNS!")
    elif (warning == 'n'):
        menu()


def ssh_instance():
    ec2 = boto3.resource('ec2')
    dns_name = input("Please enter the DNS name of the instance: ")
    instance = ec2.Instance(dns_name)
    # if (instance.state["Name"] == "running"):
    subprocess.run("scp -y -i Assignment1.pem check_webserver.py ec2-user@" +
                   dns_name + ":", shell=True)
    print("\n Successfully copied check_webserver.py script to current instance!")
    subprocess.run(
        "ssh -t -o StrictHostKeyChecking=no -i Assignment1.pem ec2-user@" + dns_name,
        shell=True)  # open up ssh again since scp command closes connection upon completion


if __name__ == '__main__':
    menu()
