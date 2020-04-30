#!/usr/bin/python3
import requests
import argparse
import os
import json
import sys
import time
from random import choice
from string import ascii_letters, digits

#Ссылка на API Majordomo
api_url = 'https://api.majordomo.ru'

#Авторизация по паре логин-пароль
def get_hms_token(hms_login, hms_passwd):
    r = requests.post("{}/oauth/token".format(api_url),
    data={'grant_type': 'password', 'client_id': 'service', 
    'client_secret': 'service_secret',
    'username':hms_login, 'password':hms_passwd})
    # Вывод полученого токена, либо описание ошибки, отправленной API 
    print(json.loads(r.text))
    return json.loads(r.text)['access_token']

def main():
    parser = argparse.ArgumentParser(description="HMS Domains")
    #Парсинг аргументов командной строки
    parser.add_argument('-i', required=True, help='Логин')
    parser.add_argument('-p', required=True, help='Пароль')
    parser.add_argument('-d', required=True, help='Имя домена, для которого создается запись')
    parser.add_argument('-o', required=True, help='ownerName, первое поле для записи в контрольной панели, должно заканчиваться на имя домена для которого создается запись.')
    parser.add_argument('-t', required=True, help='Type, тип записи ("A", "MX", "TEXT", "CNAME" и т.д.)')
    parser.add_argument('-v', required=True, help='Значение записи')
    parser.add_argument('--ttl', default='3600', help='TTL')
    parser.add_argument('--prio', default='10', help='Приоритет записи, по дефолту пустой, если надо добавить пишем значение')

    args = parser.parse_args()

    login = args.i
    password = args.p
    domain = args.d
    ownerName = args.o
    dns_type = args.t
    dns_value = args.v
    ttl = int(args.ttl)
    prio = int(args.prio)


    user_token = get_hms_token(login, password)
    #Отправка DNS записи API
    r = requests.post("{}/dns-record".format(api_url),
    headers={'Authorization': 'Bearer {}'.format(user_token)},
    json={"operationIdentity": None, "params":{"ownerName":ownerName,"type":dns_type,"data":dns_value,"ttl":ttl,"prio":prio,"name":domain}})
    #Вывод состояния операции
    print(json.loads(r.text))

    
if __name__ == "__main__":
    main()
    exit(0)