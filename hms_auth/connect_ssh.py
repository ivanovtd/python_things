import os


def connect_ssh(web, home):
    """Подключается к серверу, не эмулируя термина, nano и прочее работают корректно"""
    os.system("ssh -t {} 'sudo -Si <<< {}; sudo sh -c \"cd {} && bash -s\"'".format(web, os.environ['MJ_WEB_ROOT'], home))
