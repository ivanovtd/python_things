import requests
import decorathors
import json

class API:
    """Class that allows to work with hms API"""
    api_url = 'https://api.majordomo.ru'
    billing_token = ''


    def __init__(self, login, password):
        self.get_billing_token(login, password)


    def get_billing_token(self, billing_login, billing_password):
        r = requests.post("{}/oauth/token".format(self.api_url),
                        data={'grant_type': 'password', 'client_id': 'frontend_app',
                                'client_secret': 'frontend_app_secret',
                                'username': billing_login, 'password': billing_password})

        self.billing_token = json.loads(r.text)['access_token']

    @decorathors.get_account_id_by_name
    def request_account_id(self, account):
        params = (
            ('regex', 'true'),
            ('accountId', account),
        )

        r = requests.get('https://api.majordomo.ru/pm/accounts', 
                                headers={'Authorization': 'Bearer {}'.format(self.billing_token)}, 
                                params=params)
        return r.text

    
    @decorathors.get_id_by_domain
    def request_domains(self, domain: str) -> str:
        """Получаем id аккаунта по имени домена"""
        r = requests.get(f"{self.api_url}/domain/filter?nameContains={domain}",
                        headers={'Authorization': 'Bearer {}'.format(self.billing_token)})
        return r.text


    @decorathors.get_home_and_web
    def request_unix_account(self, account_id: str) -> [str, str]:
        """Получаем данные об аккаунте: директория и сервер"""
        r = requests.get(f"{self.api_url}/{account_id}/unix-account",
                        headers={'Authorization': 'Bearer {}'.format(self.billing_token)})
        return r.text


    @decorathors.get_email_list
    def request_user_info(self, account_id: str) -> [str]:
        """Получаем список email пользователя."""
        r = requests.get(f"{self.api_url}/{account_id}/owner/",
                        headers={'Authorization': 'Bearer {}'.format(self.billing_token)})
        return r.text

    def request_mailbox(self, account_id: str) -> [str]:
        """Получаем документ mailbox, содержащий информацию об почтовых ящиках юзверя"""
        r = requests.get(f"{self.api_url}/{account_id}/mailbox",
                headers={'Authorization': 'Bearer {}'.format(self.billing_token)})
        return r.text


    def get_server_name(self, web:str) -> str:
        """Получаем алиас сервера через API, не выгодно 5 мб по сетке таскать"""
        r = requests.get("https://api.majordomo.ru/rc-staff/server",
                         headers={'Authorization': 'Bearer {}'.format(self.billing_token)})
        servers = json.loads(r.text)
        for server in servers:
            if server['id'] == web:
                web = server['name']
                break
            else:
                continue
        return web
