import logging
import configparser
import os

LOG_FILE_NAME = 'dataCollector.log'
CONFIG_FILE_NAME = "conf.ini"

_log_format: str = f"%(asctime)s: [%(levelname)s] - (%(filename)s)." \
                   f"%(funcName)s(%(lineno)d): %(message)s"
_log_format_stream: str = f"%(asctime)s: (%(filename)s)." \
                          f"%(funcName)s(%(lineno)d): %(message)s"


def get_logger(name, file_name):
    file_info = logging.FileHandler(file_name)
    file_info.setLevel(logging.INFO)
    file_info.setFormatter(logging.Formatter(_log_format))

    file_warning = logging.FileHandler(file_name)
    file_warning.setLevel(logging.WARNING)
    file_warning.setFormatter(logging.Formatter(_log_format))

    file_error = logging.FileHandler(file_name)
    file_error.setLevel(logging.ERROR)
    file_error.setFormatter(logging.Formatter(_log_format))

    stream_info = logging.StreamHandler()
    stream_info.setLevel(logging.INFO)
    stream_info.setFormatter(logging.Formatter(_log_format_stream))

    stream_warning = logging.StreamHandler()
    stream_warning.setLevel(logging.WARNING)
    stream_warning.setFormatter(logging.Formatter(_log_format_stream))

    stream_erorr = logging.StreamHandler()
    stream_erorr.setLevel(logging.ERROR)
    stream_erorr.setFormatter(logging.Formatter(_log_format_stream))

    logger = logging.getLogger(name)
    logger.addHandler(file_info)
    logger.addHandler(file_warning)
    logger.addHandler(file_error)
    logger.addHandler(stream_info)
    # logger.addHandler(stream_warning)
    # logger.addHandler(stream_erorr)

    logger.setLevel(logging.INFO)
    return logger


def create_config(path):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "period", "10")
    with open(path, "w") as config_file:
        config.write(config_file)


def read_config(path):
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    try:
        config.read(path)
    except Exception:
        create_config(path)
        config.read(path)

    return config
