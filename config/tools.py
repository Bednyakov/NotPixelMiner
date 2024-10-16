from telethon.sync import TelegramClient, functions
from telethon.errors import SessionPasswordNeededError
from urllib.parse import unquote
from getpass import getpass

def authorization(client: TelegramClient):
    
    client.connect()

    if not client.is_user_authorized():
        phone_number = input("Введите номер телефона: +")
        client.send_code_request()

        while True:
            try:
                code = input("Введите код для входа в Telegram: ")
                if code is not None:
                    client.sign_in(phone=phone_number, code=code)
                if client.is_user_authorized():
                    break
            except SessionPasswordNeededError:  # if 2FA auth
                while True:
                    try:
                        password = getpass(prompt="Введите пароль: ")
                        client.sign_in(phone=phone_number, password=password)
                        if client.is_user_authorized():
                            break
                    except:  # if the password is wrong
                        password = None
                        code = None
                        continue
            except:  # if code is wrong
                password = None
                code = None
                continue
    return client


async def get_token(client: TelegramClient) -> str:

    # client = authorization(client)
    telegram_object = await client.get_entity("notpixel")
    webview = await client(functions.messages.RequestWebViewRequest(telegram_object, telegram_object, platform="android", url="https://notpx.app/"))
    webview_url = webview.url

    data = webview_url.split('https://notpx.app/#tgWebAppData=')[1].replace("%3D","=").split('&tgWebAppVersion=')[0].replace("%26","&")

    user_data = data.split("&user=")[1].split("&auth")[0]
    token = data.replace(user_data,unquote(user_data))
    return token


def get_headers(headers: dict, api_id: str, api_hash: str) -> dict:    
    client = TelegramClient("notpx", api_id, api_hash).start()
    token = client.loop.run_until_complete(get_token(client))
    client.disconnect()
    auth = {"Authorization": f"initData {token}"}
    headers.update(auth)
    return headers