#!/usr/bin/python3
import requests
import argparse
import os
import json
import sys
import time

billing_url = 'https://hms-billing.intr'
api_url = 'https://api.majordomo.ru'

def get_billing_token(billing_login, billing_passwd):
    r = requests.post("{}/oauth/token".format(api_url),
    data={'grant_type': 'password', 'client_id': 'frontend_app', 
    'client_secret': 'frontend_app_secret',
    'username': billing_login, 'password': billing_passwd})

    return json.loads(r.text)['access_token']

def get_user_token(billing_token, account_id):
    r = requests.post("{}/si/web-access-accounts/{}/create_token".format(api_url, account_id),
    headers={'Authorization': 'Bearer {}'.format(billing_token)})

    return json.loads(r.text)['params']['token']['access_token']

def main():
    try:
        billing_login = os.environ['MJ_BILLING_LOGIN']
        billing_passwd = os.environ['MJ_BILLING_PASSWD']
    except KeyError:
        print("Check system environment variables MJ_BILLING_LOGIN and MJ_BILLING_PASSWD")
        exit(1)

    parser = argparse.ArgumentParser(description="HMS Domains")

    parser.add_argument('-i', required=True, help='Account ID')
    parser.add_argument('-t', default='ANY', help='DNS record type')
    parser.add_argument('-d', default='ANY', help='Domain name')
    parser.add_argument('-r', help='Replace: [from] [to]', nargs='*')
    args = parser.parse_args()

    dns_type = args.t
    account_id = args.i
    domain_name = args.d
    dns_replace = False

    if account_id[0:3] == 'AC_':
        account_id = account_id[3:]

    if args.r:
        dns_replace = True
        record_old = args.r[0]
        record_new = args.r[1]

    billing_token = get_billing_token(billing_login, billing_passwd)
    user_token = get_user_token(billing_token, account_id)

    r = requests.get("{}/domain".format(api_url), 
    headers={'Authorization': 'Bearer {}'.format(user_token)})

    for domain in json.loads(r.text):
        if domain_name != domain['name'] and domain_name != 'ANY':
            continue

        for record in enumerate(domain['dnsResourceRecords']):
            if dns_type != record['rrType'] and dns_type != "ANY":
                continue

            print("[{}] {}: {}".format(record['rrType'], record['ownerName'], record['data']))
            
            if not dns_replace or record['data'] != record_old:
                continue

            del record['switchedOn']
            record['data'] = record_new

            r = requests.patch("{}/dns-record/{}".format(api_url, record['recordId']),
            headers={'Authorization': 'Bearer {}'.format(user_token)},
            json={"operationIdentity": None,"params":record})
            r = json.loads(r.text)

            print("opId: {}, actId: {}".format(r['operationIdentity'], r['actionIdentity']))

            time.sleep(5)


if __name__ == "__main__":
    main()
    exit(0)
