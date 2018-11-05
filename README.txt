READ ME - Luke Fox (20076173)

This app is menu driven and runs based off user input. The recommended usage of the app is as follows:

  1. Create an instance
  2. Add tag instance (optional)
  3. Create a bucket
  4. Add to a bucket (image.jpg provided)
  5. Move bucket image to nginx
  5. SSH into instance (to run 'check_webserver' script)
  6. Delete bucket contents
  7. Delete a bucket
  8. Delete an instance

The code for most of the menu options is sourced from the lab and modified to run based off user input.

NOTE: The 'put_bucket' method works as follows - The bucket name and the name of the object(must be inside folder containing this script) must be specified, error handling exists for both. Once both checks are met the object is uploaded. A link is then constructed from the entered bucket and object names, which is placed into an <img> tag within an echo command creating the HTML file. This file is stored inside the same folder.

NOTE: The 'move_html' method works as follows - The generated HTML file from 'put_bucket' is copied to the EC2 instance using SCP. SSH is then launched to move the HTML to the ngnix folder (not replacing the existing index file). A URL is generated using the hardcoded HTML file name and the public DNS name, and the 'webbrowser' library automatically launches this new URL.

NOTE: Some of the functions called from the menu are called with empty arguments  e.g. create_instance("")... this is to allow for user input to work(using if argument == "") while also allowing for arguments to be passed when running tests.

NOTE: Testing was ran using the command 'python3 -m pytest -s testing.py'

