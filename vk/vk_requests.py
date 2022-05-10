import os
import requests


class Get:

    def __init__(self, method, params):
        access_token = open(f"{os.getcwd()}\\vk\\Сonstants\\access_token.constant")
        api_version = open(f"{os.getcwd()}\\vk\\Сonstants\\api_version.constant")
        self.__url = f"https://api.vk.com/method/{method}?{params}&access_token={access_token.read()}" \
                     f"&v={api_version.read()}"

    def get_response(self):
        return requests.get(self.__url)


class Post:

    def __init__(self, method, content):
        access_token = open(f"{os.getcwd()}\\vk\\Сonstants\\access_token.constant")
        api_version = open(f"{os.getcwd()}\\vk\\Сonstants\\api_version.constant")
        self.__url = \
            f"https://api.vk.com/method/{method}?access_token={access_token.read()}&v={api_version.read()}"
        self.__content = content

    def get_response(self):
        return requests.post(self.__url, self.__content)


class GetAsUser:

    def __init__(self, method, params):
        user_access_token = open(f"{os.getcwd()}\\vk\\Сonstants\\user_access_token.constant")
        api_version = open(f"{os.getcwd()}\\vk\\Сonstants\\api_version.constant")
        self.__url = f"https://api.vk.com/method/{method}?{params}&access_token={user_access_token.read()}" \
                     f"&v={api_version.read()}"

    def get_response(self):
        return requests.get(self.__url)
