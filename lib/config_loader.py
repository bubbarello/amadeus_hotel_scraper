import os
import configparser

def load_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    public_config_path = os.path.join(base_dir, 'handler', 'conf', 'booking_scraper.ini')
    private_config_path = os.path.join(base_dir, 'conf_local', 'booking_scraper_local.ini')

    config = configparser.ConfigParser()
    config.read([public_config_path, private_config_path])

    return config