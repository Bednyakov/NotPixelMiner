import requests

from logger import logger


def get_status(headers: dict) -> dict|None:
    url = "https://notpx.app/api/v1/mining/status"

    for _ in range(10):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                logger.info(f"Balance: {data['userBalance']}")
                logger.info(f"Coins: {data['coins']}")
                logger.info(f"Charges: {data['charges']}")
                return data
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")
        if response.status_code == 401:
            logger.error(f"Токен просрочен: {response.status_code}")
            break

        logger.info(f"{response.status_code} Повторно запрашиваю статус...")
    logger.error(f"Ошибка get_status: {response.status_code}")


def claim(payload: dict, headers: dict) -> dict|None:
    url = "https://notpx.app/api/v1/repaint/start"

    for _ in range(10):
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            try:
                data = response.json()
                logger.info(payload)
                return data
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")
        if response.status_code == 401:
            logger.error(f"Токен просрочен: {response.status_code}")

        logger.info(f"{response.status_code} Повторно закрашиваю пиксель...")
    logger.error(f"Ошибка claim: {response.status_code}")


def get_pixel_ids(top_left: int, bottom_right: int) -> list:
    top_left_x = (top_left - 1) % 1000
    top_left_y = (top_left - 1) // 1000
    bottom_right_x = (bottom_right - 1) % 1000
    bottom_right_y = (bottom_right - 1) // 1000
    
    pixel_ids = []
    
    for y in range(top_left_y, bottom_right_y + 1):
        for x in range(top_left_x, bottom_right_x + 1):
            pixel_id = y * 1000 + x + 1
            pixel_ids.append(pixel_id)
            
    return pixel_ids