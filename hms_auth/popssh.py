import requests
import json
import sys
from API import API
import os
import argparse
"""Как работает:
    В качестве аргумента даем mailbox, парсим домен, по имени домена ищем аккаунт. Дальше ищем mailbox по апи, получаем сервер и папку, логинимся по SSH.
"""

def json_parse(mailboxes, name, domain):
    """Парсим json, полученный от api"""
    mailboxes = json.loads(mailboxes)
    for mailbox in mailboxes:
        if mailbox['name'] == name and mailbox['domain']['name'] == domain:
            return mailbox['mailSpool'], get_server_alias(mailbox['serverId'])
    print("No such mailbox^ try once more")
    exit(1)


def get_server_alias(server_name):
    aliases = {
        "mail_server_1": "pop3",
        "mail_server_3": "pop2",
        "mail_server_4": "pop1",
        "mail_server_6": "pop5"
        }
    return aliases[server_name]



def parse_mailbox(mailbox):
    """Возвращаем mailbox, разделенный по @ для парсинга домена и имени ящика, как того требует API"""
    return mailbox.split("@")


def connect_ssh(web, home):
    """Подключается к серверу, не эмулируя термина, nano и прочее работают корректно"""
    os.system(f"ssh -q -t {web} -- 'set +o history; sudo --stdin --validate --prompt='' <<< {os.environ['MJ_WEB_ROOT']}; exec -a sh sudo bash -c \"cd {home} && sudo -s\"'")



def main():

    #Парсим Аргументы
    parser = argparse.ArgumentParser(description="Mailbox name")
    parser.add_argument("mail", help="Enter email address")
    parser.add_argument("-q", help="Quiet mode, no connecton via ssh",
                        action="store_true")
    args = parser.parse_args()
    mail = args.mail
    silence = args.q

    if mail is None:
        print("Usage: popssh 123@hms.ivanovtd.ru")
        exit(1)


    mail = parse_mailbox(mail)

    api = API(os.environ['MJ_BILLING_LOGIN'],os.environ['MJ_BILLING_PASSWD'])
    acc_id = api.request_domains(mail[1])
    mailboxes = api.request_mailbox(acc_id)

    path, server = json_parse(mailboxes, mail[0], mail[1])
    print(path + '/' + mail[0], server)

    if not silence:
        connect_ssh(server, path + '/' + mail[0])


if __name__ == '__main__':
    main()

