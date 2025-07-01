class ResponseParser(object):
    @staticmethod
    def parser(response):
        status_code = response.status_code

        if status_code != 200:
            if status_code == 400:
                raise Exception(f"Bad Request (400), chiamata: {response.url}")
            elif status_code == 404:
                raise Exception(f"Not Found (404), chiamata: {response.url}")
            elif status_code == 500:
                raise Exception(f"Internal Server Error (500), chiamata: {response.url}")
            else:
                raise Exception(f"Eccezione generica ({status_code}), chiamata: {response.url}, response {response}.")

        return response.json()