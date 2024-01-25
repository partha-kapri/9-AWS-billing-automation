# Start(code)

import boto3
import click
import style
import sys
import json
import smtplib
from calendar import monthrange
from datetime import datetime
from prettytable import PrettyTable
from rich.console import Console
from fpdf import FPDF
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta

console = Console()
pt = PrettyTable()

pt.field_names = [
    'Date',
    'Account ID',
    'Services',
    'Amount(USD)',
]
pt.align = "l"
pt.align["Amount"] = "r"

aws_access_key_id = ''  # Enter your access key
aws_secret_access_key = ''  # Enter your secret access key
aws_session_token=''    #Enter your session token

# Accessing Cost Explorer API
client = boto3.client('ce',
                        aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         aws_session_token=aws_session_token)

presentday = datetime.now()
yesterday = presentday - timedelta(1)

start_date = yesterday.strftime('%Y-%m-%d')
end_date = presentday.strftime('%Y-%m-%d')

start = start_date
end = end_date

def get_cost_and_usage(bclient: client, start: str, end: str) -> list:
    cu = []
    while True:
        data = client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End':  end,
            },
            Granularity='DAILY',
            Metrics=[
                'UnblendedCost',
            ],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'LINKED_ACCOUNT',
                },
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE',
                },
            ],
        )
        cu += data['ResultsByTime']
        token = data.get('NextPageToken')
        if not token:
            break
    return cu

def fill_table_content(results: list, start: str, end: str) -> None:
    total = 0
    for result_by_time in results:
        for group in result_by_time['Groups']:
            amount = float(group['Metrics']['UnblendedCost']['Amount'])
            total += amount
            pt.add_row([
                result_by_time['TimePeriod']['Start'],
                group['Keys'][0],
                group['Keys'][1],
                format(amount, '0.2f'),
            ])
        global Estimated_grand_total 
        Estimated_grand_total = (" " "${:0.2f}".format(total))

@click.command()
@click.option('-P', '--profile', help='profile name')
@click.option('-S', '--start', help='start date (default: 1st date of current month)')
@click.option('-E', '--end', help='end date (default: last date of current month)')

def report(profile: None, start: str, end: str) -> None:
    if not start or not end:
        start = start_date
        end = end_date
    SERVICE_NAME = 'ce'
    results = get_cost_and_usage(client, start, end)
    fill_table_content(results, start, end)
    print('\n\n# Current billed resources:- \n\n')
    print(pt)
    resources = pt
    print('\n\n# Total bill:-' + Estimated_grand_total + '\n\n')

    with open("report.txt", "w") as f:
        f.write('\n\n## AWS billing report ##\n\n')
        f.write('# Current billed resources:- \n\n')
        f.write(str(resources))
        f.write('\n\n# Total bill:- ' + Estimated_grand_total)

    smtp_server = ''    # Enter your server's mail address
    smtp_port = 00      # Enter your server's port
    smtp_username = ''  # Enter your mail address
    smtp_password = ''  # Enter your mail password

    from_email = ''     # Enter the mail address from which you want to send mail
    to_email = ''   # Enter the mail address to whom you want to send mail
    subject = 'AWS billing report - ' + start
    body = 'Please see the attached report for current billed resources on AWS.'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    with open('report.txt', 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='txt')
        attachment.add_header('Content-Disposition', 'attachment', filename='report.txt')
        msg.attach(attachment)

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)

if __name__ == '__main__':
    report()

# End(code)