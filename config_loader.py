import json
from logger import *
from os.path import exists
import base64

def b64e(s):
    return base64.b64encode(s.encode()).decode()

def b64d(s):
    return base64.b64decode(s).decode()

config_data = "ewogICJCT1RUT0tFTiI6ICLQndCjINCR0JvQryDQotCe0JrQldCdINCu0JTQkCDQktCh0KLQkNCS0KwiCn0K"

if not exists("config.json"):
    logging.info("config.json not found")

    try:
        with open("config.json", "w", encoding="utf-8") as config:
            config.write(b64d(config_data))

        logging.info("config.json has been created")

    except Exception as e:
        logging.error(f"Failed to create config.json: {e}")

try:
    with open("config.json", "r", encoding="utf-8") as file:
        config: dict[str: any] = json.load(file)
        logging.info("config.json loaded successfully")

except FileNotFoundError:
    logging.critical("config.json not found.")
except json.JSONDecodeError as e:
    logging.critical(f"Error parsing JSON: {e}")
except Exception as e:
    logging.critical(f"Unexpected error while loading config.json: {e}")