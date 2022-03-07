import json
import os
import requests
from vk.vk_requests import Get


class LongpollServer:

    def __init__(self):
        group_id = open(f"{os.getcwd()}\\Constants\\group_id.constant")
        api_version = open(f"{os.getcwd()}\\Constants\\api_version.constant")
        get = Get("messages.getLongPollServer",
                  f"need_pts=0&group_id={group_id.read()}&lp_version=3&v={api_version.read()}")
        longpoll_server_response = json.loads(get.get_response().text)["response"]
        self.__server = longpoll_server_response["server"]
        self.__key = longpoll_server_response["key"]
        self.__ts = longpoll_server_response["ts"]

    def get_server(self):
        return self.__server

    def get_key(self):
        return self.__key

    def get_update(self):
        event = json.loads(requests.get(f"https://{self.__server}?act=a_check&key={self.__key}"
                                        f"&ts={self.__ts}&wait=25&mode=130&version=3").text)
        try:
            self.__ts = event["ts"]
            return event["updates"]
        except KeyError:
            if event["failed"] == 4:
                print("Изменилась актуальная версия лонгпол сервера")
            return None
