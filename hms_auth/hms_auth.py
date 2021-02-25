#!python3
import json
import os
import argparse
import requests
import re
import connect_ssh as con 
from API import API
import decorathors

def get_server_name(web) -> str:
    """ Возвращает алиас сервера по id
    # Достаточно противоречивое место. Если видите, что id серверов обновляются часто,
    # то можно использовать API, но учитывайте, что оно отдает 5 Мб (100000 строк)
    # Для получения алиаса через API вместо     web = get_server_name(web)
    # Вставляем web = api.get_server_name(web)
    """
    aliases = {
        "db_server_20": "mdb4",
        "5821f8c596ccde0001c82a61": "web99",
        "584eb62d96ccde00012776f7": "mailstor",
        "web_server_114": "web15",
        "web_server_53": "baton",
        "web_server_115": "web16",
        "web_server_116": "web17",
        "web_server_117": "web18",
        "web_server_118": "web19",
        "web_server_120": "web20",
        "web_server_121": "web21",
        "web_server_122": "web22",
        "web_server_123": "web23",
        "web_server_124": "staff",
        "web_server_125": "web24",
        "web_server_126": "web25",
        "web_server_127": "web26",
        "web_server_128": "web27",
        "web_server_129": "web28",
        "web_server_130": "web29",
        "web_server_131": "web30",
        "web_server_132": "web31",
        "web_server_133": "web32",
        "web_server_134": "web33",
        "web_server_135": "web34",
        "web_server_136": "web35",
        "59088b33719fca053cf2229a": "web36",
        "mail_server_1": "pop3",
        "mail_server_3": "pop2",
        "mail_server_4": "pop1",
        "mail_server_6": "pop5",
        "web_server_138": "web37",
        "5d1cc4a6e1442a0001c88634": "kvm-test",
    }
    return aliases[web]


def is_domain(text) -> bool:
    """Проверяет является ли строка доменом"""
    return re.match(r".+\..+", text) is not None


def get_api_data(data) -> [str, str, str]:
    """Функция получающая данные с API"""
    try:
        billing_login = os.environ['MJ_BILLING_LOGIN']
        billing_passwd = os.environ['MJ_BILLING_PASSWD']
    except KeyError:
        print("Check system environment variables MJ_BILLING_LOGIN and MJ_BILLING_PASSWD")
        exit(1)
    account_id = None
    api = API(billing_login, billing_passwd)
    if is_domain(data):
        account_id = api.request_domains(data.lower())
    if account_id is None:
        account_id = api.request_account_id(re.sub(r'[^0-9.]+', r'', data))
    print("AC_" + account_id)
    mail = api.request_user_info(account_id)
    home, web = api.request_unix_account(account_id)
    web = get_server_name(web)
    print(f'URL: https://hms-billing.intr/account/{account_id}')
    return mail, home, web


def main():
    #Парсим Аргументы
    parser = argparse.ArgumentParser(description="HMS Login")
    parser.add_argument("ac", help="Enter account name/domain")
    parser.add_argument("-q", help="Quiet mode, no connecton via ssh",
                        action="store_true")
    args = parser.parse_args()
    data = args.ac
    silence = args.q

    if data is None:
        print("Usage: webssh ( AC_224436 || 224436 || ivanovtd.ru)")
        exit(1)

    mail, home, web = get_api_data(data)

    print(f"Emails are: {mail}")
    print(home + '  ' + web)

    if not silence:
        print('\n')
        print('\n')
        print('\n')
        con.connect_ssh(web, home)


if __name__ == "__main__":
    main()
