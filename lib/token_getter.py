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
        """
        Main method to get a token, checks if there's a valid token inside the config file
        otherwise generates a new one
        :return: The access token
        """
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
        """
        Method to generate a new token and save it inside the local config file
        :return: The access token
        """
        # Genera token
        token_request = requests.post(self.token_url, headers=self.headers, data=self.body)
        token_json = lib.response_parser.ResponseParser.parser(token_request)

        access_token = token_json.get("access_token")
        if not access_token:
            raise Exception("Token non presente nella response")

        # Aggiorna il file conf_local con il token nuovo
        lib.config_loader.write_to_private_config('Token', 'token', access_token)

        return access_token