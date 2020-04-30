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
    # Перед запуском программы добавить в переменные окружения MJ_BILLING_LOGIN и MJ_BILLING_PASSWD
    # Это можно сделать в .bashrc/.zshrc/.bash_profile и т.д.
    try:
        billing_login = os.environ['MJ_BILLING_LOGIN']
        billing_passwd = os.environ['MJ_BILLING_PASSWD']
    except KeyError:
        print("Check system environment variables MJ_BILLING_LOGIN and MJ_BILLING_PASSWD")
        exit(1)

    parser = argparse.ArgumentParser(description="HMS Domains")

    parser.add_argument('-i', required=True, help='Account ID')
    parser.add_argument('-s', required=True, help='Subdomain name eg sub.domain.com')
    parser.add_argument('-l', default="3", help='Subdomain level, default: 3')
    args = parser.parse_args()

    account_id = args.i
    subdomain_name = args.s
    level = int(args.l) - 1

    if account_id[0:3].upper() == 'AC_':
        account_id = account_id[3:]


    billing_token = get_billing_token(billing_login, billing_passwd)
    user_token = get_user_token(billing_token, account_id)

    r = requests.get("{}/domain".format(api_url), 
    headers={'Authorization': 'Bearer {}'.format(user_token)})    
    subdomain_exist = False
    parent_exist = False

    parent_domain = '.'.join(subdomain_name.split('.')[level-1:])

    for domain in json.loads(r.text):
        #Проверка на существование родителя, если существует ставим родителя в parent_domain
        if parent_domain == domain['name']:
            parent_domain = domain
            parent_exist = True

        #Проверка на существование поддомена
        if subdomain_name in domain['name']:
            print("Subomain already exist")
            subdomain_exist = True
            
    # Вывод ошибки о несуществовании родителя     
    if not parent_exist:
        print('.'.join(subdomain_name.split('.')[level-1:]) + " doesn\'t exist!")



    if not subdomain_exist and parent_exist:
        
        #Поддомен делаем на основе родительского домена
        new_subdomain = {'name': '.'.join(subdomain_name.split('.')[0:-2]), 'parentDomainId':parent_domain['id']}
        print(new_subdomain)
        
        #Отправка поддомена
        r = requests.post("{}/domain".format(api_url),
        headers={'Authorization': 'Bearer {}'.format(user_token)},
        json={"operationIdentity": None, "params":new_subdomain})

        print(r.text)

        time.sleep(5)


if __name__ == "__main__":
    main()
    exit(0)
