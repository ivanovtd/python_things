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

if len(sys.argv) != 2:
        sys.stderr.write(
            "syntax: vmip.py vm_name, ip_address or domain_name\n")
        sys.exit(1)
vm = sys.argv[1].strip()

# Получаем данные и приводим их в божеский вид
acc_info, acc_passwords = get_vm_data.get_data()
acc_info = json.loads(acc_info)
acc_passwords = json.loads(acc_passwords)

# Извлекаем полезную информацию, в частности: ID клиента, ID VPS, IP адрес, и делаем линк в биллинг
client_id = acc_info['vds_account']['client_id']
vm_id = acc_info['vds_account']['vds_account_id']
ip = acc_info['vds_account']['primary_ip_address']['address']
print(f"Billing link: https://billing2.intr/client/{client_id}/vds/account/{vm_id}")
print(f"IP address: {ip}")

passwords = []
for item in acc_passwords['vds_passwords']:
    passwords.append({
        'subj': bytes(item['subject'], 'iso-8859-1').decode('utf8'),
        'login': item['login'],
        'password': item['password']
    })

for pw in passwords:
    pprint(pw)


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
