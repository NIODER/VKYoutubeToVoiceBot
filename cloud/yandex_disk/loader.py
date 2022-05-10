import yadisk.yadisk
import os


class YandexLoader:

    def __init__(self):
        self.__directory = "/mireabot/videos/"
        s = 'cloud\\yandex_disk'
        token = open(f"{os.getcwd()}\\vk\\Сonstants\\yandex_disk_token.constant")
        self.y = yadisk.YaDisk(token=token.read())

    def load(self, file):
        if not self.y.is_dir(self.__directory):
            self.y.mkdir(self.__directory)
        path = self.__directory + file
        self.y.upload(f"{os.getcwd()}\\download\\video\\{file}.mp4", path)
        return self.y.publish(path=path)
