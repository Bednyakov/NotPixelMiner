from random import randint, choice
from dotenv import load_dotenv
from time import sleep
import os

from templates import top_left, bottom_right, colors
from .claim import get_status, claim, get_pixel_ids
from config import get_headers, headers
from logger import logger

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

def main():
    if not API_ID or not API_HASH:
        raise ValueError("API_ID и API_HASH не подгрузились!")
    
    break_count = 3
    
    while break_count > 0:

        new_headers = get_headers(headers, api_id=API_ID, api_hash=API_HASH)
        status_data = get_status(new_headers)
        if status_data:
            charges = int(status_data["charges"])

            for _ in range(charges):

                id: int = choice(get_pixel_ids(top_left=top_left, bottom_right=bottom_right))
                color: str = choice(colors)
                payload = {"pixelId": id, "newColor": color}
                
                data = claim(headers=new_headers, payload=payload)
                sleep(randint(3, 21))

            logger.info(f"Balance: {data['balance']}")
            logger.info("Копим пиксели...")

            break_count = 3
            sleep(randint(605, 3650))
        
        break_count -= 1

    logger.error("Превышено число попыток подключения к клиенту Telegram.")