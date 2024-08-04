The following program needs the URLs of the appointments that you need to look out for. The console output will display when the appointments are available. The program runs every 10 mins using python selenium.

**How to run:**

You need to install python, chrome (latest version), chrome webdriver (compatible with chrome version).

First, create a virtual environment and activate it. Using the following document to create a virtual environment: https://docs.python.org/3/library/venv.html

Then run: 

    pip install -r requirements.txt
    python selenium_test.py

Then create a `.env` file and add the following to it:

    RECEIVER_EMAIL="<Receiver's email address>"
    SENDER_EMAIL="<Sender's email address>"
    SENDER_EMAIL_PASSWD="<Sender's email password>"
