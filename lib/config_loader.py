import os
import configparser

def load_config():
    """
    Auto loader config file
    :return: ConfigParser instance
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    public_config_path = os.path.join(base_dir, 'handler', 'conf', 'booking_scraper.ini')
    private_config_path = os.path.join(base_dir, 'conf_local', 'booking_scraper_local.ini')

    config = configparser.ConfigParser()
    config.read([public_config_path, private_config_path])

    return config


def get_private_config_path():
    """
    Return private config path
    :return: Private config path
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'conf_local', 'booking_scraper_local.ini')


def write_to_private_config(section, option, value):
    """
    Write value to private config file
    :param section: Section name
    :param option: Option name
    :param value: Value to write
    """
    config_path = get_private_config_path()
    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.has_section(section):
        config.add_section(section)

    config.set(section, option, value)

    with open(config_path, 'w') as f:
        config.write(f)