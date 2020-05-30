#!/usr/bin/python3

#Для корректной работы скрипта необходимо установить sshpass, pexpect
#sudo apt install sshpass
#python3 -m pip install pexpect 
#соответственно
#В переменных окружения должен быть указан пароль и логин от билинга, MJ_BILLING_LOGIN & MJ_BILLING_PASSWD соответственно.
import json
import os
import sys
from pprint import pprint
import get_vm_data
import argparse

def connect_ssh(passwords, ip):
    #Получаем последний пароль для пользователя root, обращаем внимание, что это также может быть
    #Пароль от mysql/pgsql/чего угодно, поэтому если не подключается попробуйте ручками.
    for i in passwords:
        if i['login'] == 'root':
            ROOT_PASS = i['password']

    print('Root pass: ' + ROOT_PASS)

    #Авторизация по ssh используя sshpass, в Windows можно изменить на putty, к примеру:
    """os.system(f'putty -load "{ip}" -l root -pw {ROOT_PASS}')"""

    if ROOT_PASS:
        os.system(f"sshpass -p {ROOT_PASS} ssh -o StrictHostKeyChecking=no root@{ip}")
    else:
        print("No root password detected")


def main():
    # Парсим аргументы
    parser = argparse.ArgumentParser()
    parser.add_argument("vm", help="Enter ip/vm name/domain")
    parser.add_argument("-c", help="Connection mode", action="store_true")
    args = parser.parse_args()
    vm = args.vm
    con = args.c
    
    # Получаем данные
    acc_info, acc_passwords = get_vm_data.get_data(vm)
    # Извлекаем полезную информацию, в частности: ID клиента, ID VPS, IP адрес, пароли и делаем линк в биллинг
    acc_info = json.loads(acc_info)
    acc_passwords = json.loads(acc_passwords)
    client_id = acc_info['vds_account']['client_id']
    vm_id = acc_info['vds_account']['vds_account_id']
    ip = acc_info['vds_account']['primary_ip_address']['address']
    passwords = []
    for item in acc_passwords['vds_passwords']:
        passwords.append({
            'subj': bytes(item['subject'], 'iso-8859-1').decode('utf8'),
            'login': item['login'],
            'password': item['password']
        })
    #Принтим список паролей, ip, ссылку на биллинг
    print(f"Billing link: https://billing2.intr/client/{client_id}/vds/account/{vm_id}")
    print(f"IP address: {ip}")
    for pw in passwords:
        pprint(pw)

    if con:
        connect_ssh(passwords, ip)

if __name__ == '__main__':
    main()

