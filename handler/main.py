import requests
import lib.utils
import lib.response_parser
import lib.token_getter
import lib.config_loader

class ScraperAmadeus(object):
    def __init__(self):
        self.config = lib.config_loader.load_config()
        self.url_hotel_by_city = self.config.get("Amadeus", "url_hotel_by_city")
        self.url_hotel_by_id = self.config.get("Amadeus", "url_hotel_by_id")
        self.n_adulti = self.config.get("Filters", "n_adulti")

    def get_hotel_by_city(self, city_code, days="7"):
        # Upper alla sicura
        city_code = city_code.upper()

        # Istanza response parser
        response_parser = lib.response_parser.ResponseParser()

        # Generazione Authorization Bearer
        token = lib.token_getter.TokenGetter().generate_token()
        headers = {"Authorization": "Bearer" + token}

        request_hotel_by_city = requests.get(
            self.url_hotel_by_city.replace("{{city_code}}", city_code),
            headers=headers
        )
        response_hotel_by_city = response_parser.parser(request_hotel_by_city)

        hotel_ids_str = lib.utils.list_hotel_ids_as_string(response_hotel_by_city)

        request_hotels_ids = requests.get(
            self.url_hotel_by_id
                .replace("{{hotel_ids_str}}", hotel_ids_str)
                .replace("{{n_adulti}}", self.n_adulti),
            headers=headers
        )
        response_hotel_by_ids = response_parser.parser(request_hotels_ids)

        return response_hotel_by_ids

if __name__ == "__main__":
    scraper = ScraperAmadeus()
    hotels_tokyo_7_days = scraper.get_hotel_by_city('HDN')
    hotels_osaka_4_days = scraper.get_hotel_by_city('ITM', days="4")
    hotels_tokyo_4_days = scraper.get_hotel_by_city('HDN', days="4")
    print(hotels_tokyo_7_days)
    print(hotels_osaka_4_days)
    print(hotels_tokyo_4_days)