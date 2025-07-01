import requests
import lib.config_loader
import lib.response_parser

class TokenGetter(object):
    def __init__(self):
        self.config = lib.config_loader.load_config()
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.token_url = self.config.get("Token", "token_url")
        self.api_key = self.config.get('API', 'api_key')
        self.api_secret = self.config.get('API', 'api_secret')

        self.body = {
            "client_id": self.api_key,
            "client_secret": self.api_secret,
            "grant_type": "client_credentials"
        }

    def get_token(self):
        token = self.config.get("Token", "token", fallback=None)
        response_parser = lib.response_parser.ResponseParser()

        # Check token esistente e vedi se è scaduto in caso genera nuovo
        if token:
            token_check = requests.get(f"{self.token_url}/{token}", headers=self.headers)
            token_check_json = response_parser.parser(token_check)
            if token_check_json.get('state') == 'expired':
                return self.generate_token()
            else:
                return token
        else:
            return self.generate_token()

    def generate_token(self):
        # Genera token
        token_request = requests.post(self.token_url, headers=self.headers, data=self.body)
        token_json = lib.response_parser.ResponseParser.parser(token_request)

        access_token = token_json.get("access_token")
        if not access_token:
            raise Exception("Token non presente nella response")

        # Aggiorna il file ini
        if not self.config.has_section('Token'):
            self.config.add_section('Token')
        self.config.set('Token', 'token', access_token)

        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

        return access_token