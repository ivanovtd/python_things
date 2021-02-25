import os


def connect_ssh(web, home):
    """Подключается к серверу, не эмулируя термина, nano и прочее работают корректно"""
    os.system(f"ssh -q -t {web} -- 'set +o history; sudo --stdin --validate --prompt='' <<< {os.environ['MJ_WEB_ROOT']}; exec -a sh sudo bash -c \"cd {home} && sudo -s\"'")

