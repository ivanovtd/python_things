#!/usr/bin/python3
import json
import os
import pexpect
import re
import socket
import ssl
import sys
import xmlrpc.client
ALIASES = {"20226": "20327"}
rpc_server = 'https://rpc-mj.intr/'
rpc_user = os.environ['MJ_BILLING_LOGIN']
rpc_pass = os.environ['MJ_BILLING_PASSWD']


class my_https_transport(xmlrpc.client.SafeTransport):
    def __init__(self, use_datetime=0):
        xmlrpc.client.SafeTransport.__init__(self, use_datetime)
        self._cookie = None
        self._extra_headers = []

    def set_cookie(self, cookie):
        self._cookie = cookie

    def send_headers(self, connection, headers):
        if self._cookie:
            headers.append(('Cookie', 'RPCSID=%s' % self._cookie))
        for key, val in headers:
            connection.putheader(key, val)


def is_ip(text):
    result = re.match(r"(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})", text)
    if result is None:
        return False
    i = 1
    while i <= 4:
        if int(result.group(i)) < 0 or int(result.group(i)) > 255:
            return False
        i += 1
    return True


def is_domain_name(text):
    return re.match(r".+\..+", text) is not None


def get_data(vm):
    vm_ip = None
    vm_name = None
    if is_ip(vm):
        vm_ip = vm
    else:
        if vm[:2] == "vm":
            vm_tmp = vm[2:]
        else:
            vm_tmp = vm
        result = re.match(r"(\d{2,7})(\.majordomo\.ru|\.mj-host\.ru)?", vm_tmp)
        if result is not None:
            vm_name = result.group(1)
            if vm_name in ALIASES:
                vm_name = ALIASES[vm_name]
        elif is_domain_name(vm):
            vm_ip = socket.gethostbyname(vm)
        else:
            sys.stderr.write("wrong vm name, ip or domain name\n")
            sys.exit(1)
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    xml = xmlrpc.client.ServerProxy(rpc_server)
    session = xml.authentication.login(rpc_user, rpc_pass).get('session_id')
    t = my_https_transport()
    t.set_cookie(session)
    xml = xmlrpc.client.ServerProxy(rpc_server, transport=t)
    if vm_ip is not None:
        retcode = xml.clients.search_client(vm_ip)
        vm_name = retcode["clients"][0]["va_vds_account_id"]
        retcode = xml.vds.get_account(vm_name)
        acc_info = json.dumps(retcode, ensure_ascii=False)
        #adm = retcode["vds_account"]["plan"]["adm"]
    else:
        retcode = xml.vds.get_account(vm_name)
        acc_info = json.dumps(retcode, ensure_ascii=False)
    acc_passwords = json.dumps(xml.vds.get_passwords(vm_name))
    xml.authentication.logout()
    return acc_info, acc_passwords

