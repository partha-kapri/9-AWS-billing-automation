# Start(code)

import boto3
import click
import style
import sys
from calendar import monthrange
from datetime import datetime
from prettytable import PrettyTable
from rich.console import Console
from fpdf import FPDF
console = Console()
pt = PrettyTable()

pt.field_names = [
    'TimePeriodStart',
    # 'TimePeriodEnd',
    'LinkedAccount',
    'Service',
    'Amount(USD)',
]
pt.align = "l"
pt.align["Amount"] = "r"

def get_cost_and_usage(bclient: object, start: str, end: str) -> list:
    cu = []
    while True:
        data = bclient.get_cost_and_usage(
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
                }
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
            if amount < 0.00001:
                continue
            pt.add_row([
                result_by_time['TimePeriod']['Start'],
                # result_by_time['TimePeriod']['End'],
                group['Keys'][0],
                group['Keys'][1],
                format(amount, '0.2f'),
            ])
    console.print("Estimated grand total:" " " "${:0.2f}".format(total),style="bold red")

@click.command()
@click.option('-P', '--profile', help='profile name')
@click.option('-S', '--start', help='start date (default: 1st date of current month)')
@click.option('-E', '--end', help='end date (default: last date of current month)')

def report(profile: str, start: str, end: str) -> None:
    if not start or not end:
        ldom = monthrange(datetime.today().year, datetime.today().month)[1]
        start = datetime.today().replace(day=1).strftime('%Y-%m-%d')
        end = datetime.today().replace(day=ldom).strftime('%Y-%m-%d')
    SERVICE_NAME = 'ce'
    bclient = boto3.Session(profile_name=profile).client(SERVICE_NAME)
    results = get_cost_and_usage(bclient, start, end)
    fill_table_content(results, start, end)
    print(pt)

if __name__ == '__main__':
    report()

# End(code)