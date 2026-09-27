#todo/config.py

import configparser
from pathlib import Path
import typer
from todo import __app_name__, DB_WRITE_ERROR,SUCCESS,DIR_ERROR,FILE_ERROR

CONFIG_DIR = Path(typer.get_app_dir(__app_name__))
CONFIG_PATH = CONFIG_DIR / "config.ini"

def init_app(db_path: str) -> int :
    """Initialize the application by creating the configuration directory and file if they don't exist."""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    database_code = _create_database(db_path)
    if database_code != SUCCESS:
        return database_code
    return SUCCESS

def _init_config_file() -> int :
    try:
        CONFIG_DIR.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try :
        CONFIG_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS

def _create_database(db_path: str) -> int :
    config_parser = configparser.ConfigParser()
    config_parser['General'] = {'database': db_path}
    try:
        with CONFIG_PATH.open('w') as config_file:
            config_parser.write(config_file)
    except OSError:
        return DB_WRITE_ERROR
    return SUCCESS