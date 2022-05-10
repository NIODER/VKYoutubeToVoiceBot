from cloud.yandex_disk.loader import YandexLoader


def create_loader(name):
    if name == "yandex":
        return YandexLoader()
    else:
        raise Exception('no such service')
