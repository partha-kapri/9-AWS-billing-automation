# Project-9-AWS-billing-automation

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

## Usage

```bash
$ ./main.py --help

Usage: main.py [OPTIONS]

Options:
  -P, --profile TEXT  profile name
  -S, --start TEXT    start date (default: 1st date of current month)
  -E, --end TEXT      end date (default: last date of current month)
  --help              Show this message and exit.
```

## Examples

check the report of date range [2024-01-04, 2024-01-05]

```bash
$ ./main.py -P my-profile -S 2024-01-04 -E 2024-01-05

Estimated grand total: $0.88
+-----------------+---------------+-------------------+-------------+
| TimePeriodStart | LinkedAccount | Service           | Amount(USD) |
+-----------------+---------------+-------------------+-------------+
| 2024-01-04      | 324680976314  | AWS Cost Explorer | 0.88        |
+-----------------+---------------+-------------------+-------------+

```
