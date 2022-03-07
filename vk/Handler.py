import json
import os
import random
import pytube.exceptions
import requests
from vk.vk_requests import Post, Get
from pytube import YouTube
from moviepy.editor import VideoFileClip


class Handler:

    def __init__(self, updates):
        for update in updates:
            self.__handle(update)

    def __handle(self, update):
        if update[0] == 4:
            if update[2] == 3:
                return
            self.__message_arrived(update)

    @staticmethod
    def __message_arrived(update):
        peer_id = update[3]
        try:
            if update[7]["attach1_type"] == "video":
                Handler.__send_message(peer_id, "Видео нужно отправлять без вложения")
                return
        except KeyError:
            url = Handler.__beautify_url(update[5])
            Handler.__send_message(peer_id, "Конвертирую...")
            try:
                # скачиваем видео
                video = YouTube(url)
                title = Handler.__beautify(video.title)
                video = video.streams.filter(progressive=True, file_extension="mp4").order_by(
                    "resolution").desc().first()
                video.download(f"{os.getcwd()}\\download\\video")
                video = VideoFileClip(f"{os.getcwd()}\\download\\video\\{title}.mp4")
                audio = video.audio
                audio.write_audiofile(f"{os.getcwd()}\\download\\audio\\{title}.mp3")
                video.close()
                audio.close()
                # создаем и отправляем голосовое
                upload_server = json.loads(
                    Get("docs.getMessagesUploadServer", f"type=audio_message&peer_id={peer_id}").get_response().text
                )["response"]["upload_url"]
                request = requests.post(upload_server,
                                        files={
                                            "file": open(f"{os.getcwd()}\\download\\audio\\{title}.mp3", "rb")}).json()
                save = json.loads(
                    Post("docs.save", {"file": request["file"]}).get_response().text
                )["response"]["audio_message"]
                d = "doc" + str(save["owner_id"]) + "_" + str(save["id"])
                Post("messages.send",
                     {"peer_id": peer_id, "attachment": d, "random_id": random.randint(1, 2147483646)}).get_response()
                # очищаем место на диске
                os.remove(f"{os.getcwd()}\\download\\video\\{title}.mp4")
                os.remove(f"{os.getcwd()}\\download\\audio\\{title}.mp3")
            except pytube.exceptions.RegexMatchError:
                Handler.__send_message(peer_id, "Неправильная ссылка")

    @staticmethod
    def __send_message(peer_id, message):
        return Post("messages.send",
                    {
                        "user_id": peer_id,
                        "random_id": random.randint(1, 2147483646),
                        "peer_id": peer_id,
                        "message": message
                    }).get_response()

    @staticmethod
    def __beautify(old_name):
        chars = ["<", ">", ":", "\"", "\\", "/", "|", "?", "*", "0", ","]
        for char in chars:
            old_name = str(old_name).replace(char, "")
        return old_name

    @staticmethod
    def __beautify_url(url):
        return str(url).replace("www.youtube.com/watch?v=", "youtu.be/")
