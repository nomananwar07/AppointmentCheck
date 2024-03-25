The following program needs the URLs of the appointments that you need to look out for. The console output will display when the appointments are available. The program runs every 5 mins using python selenium.

## How to run:

You need to install python, chrome (latest version), chrome webdriver (compatible with chrome version).

First, create a virtual environment and activate it. Using the following document to create a virtual environment: https://docs.python.org/3/library/venv.html

Then run: 

    pip install -r requirements.txt
    python selenium_test.py
  
## Troubleshoot

If you are facing alot of 
#### "... not able to get the click button because of internet issue. Increase the retries limit" 
warning even after increasing the retries limit.
Switch to **moreRobust** branch, that program will run slow but is able to handle such issues.