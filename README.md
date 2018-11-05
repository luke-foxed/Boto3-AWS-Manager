# Boto3-AWS-Manager

This app is menu driven and runs based off user input. It allows for the user to create new EC2 instances, tag those instances and delete them. 

It also allows for the user to create S3 buckets and populate those buckets. From there, the user can SSH into an ec2 instance, which will start an NGINX server and move any image from
the specified bucket into a new html file within the NGINX server - and then load that html file containing the bucket image.

The app also features a resource monitoring script (check_webserver.py) to be used upon SSHing into an instance to measure things such as CPU usage and whether various services are running or not.

The recommended usage of the app is as follows:

  - Create an instance
  - Add tag instance (optional)
  - Create a bucket
  - Add to a bucket (such as an image)
  - Move bucket image to nginx
  - SSH into instance (to run 'check_webserver' script)
  - Delete bucket contents
  - Delete a bucket
  - Delete an instance
  
  
 ----

**NOTE**: The 'put_bucket' method works as follows - The bucket name and the name of the object(must be inside folder containing this script) must be specified, error handling exists for both. Once both checks are met the object is uploaded. A link is then constructed from the entered bucket and object names, which is placed into an <img> tag within an echo command creating the HTML file. This file is stored inside the same folder.

**NOTE**: The 'move_html' method works as follows - The generated HTML file from 'put_bucket' is copied to the EC2 instance using SCP. SSH is then launched to move the HTML to the ngnix folder (not replacing the existing index file). A URL is generated using the hardcoded HTML file name and the public DNS name, and the 'webbrowser' library automatically launches this new URL.

**NOTE**: Some of the functions called from the menu are called with empty arguments  e.g. create_instance("")... this is to allow for user input to work(using if argument == "") while also allowing for arguments to be passed when running tests.

**NOTE**: Testing was ran using the command 'python3 -m pytest -s testing.py'
