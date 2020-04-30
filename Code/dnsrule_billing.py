#!/usr/bin/python3
import requests
import argparse
import os
import json
import sys
import time
from random import choice
from string import ascii_letters, digits

"""Запуск скрипта: python3 dnsrule.py -i AC_224436 -d ivanovtd.ru -o xxx.ivanovtd.ru -t A -v 8.8.8.8
Сразу обращаем внимание на параметр -о, он должени иметь вид xxx.domain.com для домена domain.com
"""


#Ссылка на API Majordomo и API billing
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
    print(json.loads(r.text))
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
    #Парсинг аргументов командной строки
    parser.add_argument('-i', required=True, help='Логин')
    parser.add_argument('-d', required=True, help='Имя домена, для которого создается запись')
    parser.add_argument('-o', required=True, help='ownerName, первое поле для записи в контрольной панели, должно заканчиваться на имя домена для которого создается запись.')
    parser.add_argument('-t', required=True, help='Type, тип записи ("A", "MX", "TEXT", "CNAME" и т.д.)')
    parser.add_argument('-v', required=True, help='Значение записи')
    parser.add_argument('--ttl', default='3600', help='TTL')
    parser.add_argument('--prio', default='10', help='Приоритет записи, по дефолту пустой, если надо добавить пишем значение')

    args = parser.parse_args()

    account_id = args.i
    domain = args.d
    ownerName = args.o
    dns_type = args.t
    dns_value = args.v
    ttl = int(args.ttl)
    prio = int(args.prio)

    if account_id[0:3].upper() == 'AC_':
        account_id = account_id[3:]



    billing_token = get_billing_token(billing_login, billing_passwd)
    user_token = get_user_token(billing_token, account_id)

    #Отправка DNS записи API
    r = requests.post("{}/dns-record".format(api_url),
    headers={'Authorization': 'Bearer {}'.format(user_token)},
    json={"operationIdentity": None, "params":{"ownerName":ownerName,"type":dns_type,"data":dns_value,"ttl":ttl,"prio":prio,"name":domain}})
    #Вывод состояния операции
    print(json.loads(r.text))

    
if __name__ == "__main__":
    main()
    exit(0)