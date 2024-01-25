#AWS-billing-automation

## Prerequisites
- Python 3.10 (or later)


## Setup Requirements
```bash
$ pipenv install
```

or

```bash
$ pip3 install -r requirements.txt
```


### Enter the credentials
```bash

# Specify your AWS credentials 
aws_access_key_id = '' # Enter your access key
aws_secret_access_key = '' # Enter your secret access key
aws_session_token = '' # Enter your session token

```


## Setup the mail service

```bash
smtp_server = ''    # Enter your server's mail address
smtp_port = 00      # Enter your server's port
smtp_username = ''  # Enter your mail address
smtp_password = ''  # Enter your mail password

from_email = ''     # Enter the mail address from which you want to send mail
to_email = ''   # Enter the mail address to whom you want to send mail
```


## Then run the script using below command

```bash
$ python3 main.py

```

