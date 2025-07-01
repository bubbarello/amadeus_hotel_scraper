class ResponseError(Exception):
    """Base class for response errors."""
    def __init__(self, status_code, url, message=None):
        self.status_code = status_code
        self.url = url
        self.message = message or f"HTTP {status_code} Error for URL: {url}"
        super().__init__(self.message)

class BadRequestError(ResponseError):
    pass

class NotFoundError(ResponseError):
    pass

class InternalServerError(ResponseError):
    pass

class GenericResponseError(ResponseError):
    pass

class ResponseParser(object):
    @staticmethod
    def parser(response):
        """
        Parse the response and return a dictionary with the parsed data.
        :param response: Response from the request library.
        :return: Parsed response if status_code equals 200 exception otherwise.
        """
        status_code = response.status_code
        url = response.url

        if status_code != 200:
            if status_code == 400:
                raise BadRequestError(status_code, url, f"Bad Request (400) - URL: {url}")
            elif status_code == 404:
                raise NotFoundError(status_code, url, f"Not Found (404) - URL: {url}")
            elif status_code == 500:
                raise InternalServerError(status_code, url, f"Internal Server Error (500) - URL: {url}")
            else:
                raise GenericResponseError(status_code, url, f"Unexpected HTTP {status_code} - URL: {url}")

        return response.json()