import json

def get_home_and_web(get_data):
    def wraper(self, account_id):
        data = json.loads(get_data(self, account_id))
        return data[0]['homeDir'], data[0]['serverId']
    return wraper


def get_id_by_domain(get_data):
    def wraper(self, domain):
        domain_list = json.loads(get_data(self, domain))
        for domains in domain_list:
            if domains['name'] == domain:
                print(domains['name'])
                account_id = domains['accountId']
                break
            else:
                continue
        return account_id
    return wraper


def get_email_list(get_data):
    def wraper(self, account_id):
        data = json.loads(get_data(self, account_id))
        email = data['contactInfo']['emailAddresses']
        return email
    return wraper