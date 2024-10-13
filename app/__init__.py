from random import randint, choice
from dotenv import load_dotenv
from time import sleep
import os

from .claim import get_status, claim
from config import get_headers, headers
from logger import logger

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

if not API_ID or not API_HASH:
    raise ValueError("API_ID и API_HASH не подгрузились!")

def main():
    while True:

        new_headers = get_headers(headers, api_id=API_ID, api_hash=API_HASH)
        status_data = get_status(new_headers)
        charges = int(status_data["charges"])

        for _ in range(charges):

            id: int = randint(1, 1000000)
            color: str = choice(["#E46E6E", "#FFD635", "#7EED56", "#00CCC0", "#51E9F4", "#94B3FF", "#E4ABFF", "#FF99AA", "#FFB470", "#FFFFFF"])
            payload = {"pixelId": id, "newColor": color}
            
            data = claim(headers=new_headers, payload=payload)
            sleep(randint(3, 21))

        logger.info(f"Balance: {data['balance']}")
        logger.info("Копим пиксели...")   
        sleep(randint(605, 3650))