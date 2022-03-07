from vk.Handler import Handler
from vk.longpoll_server import LongpollServer

if __name__ == "__main__":
    # подключение к лонгпол уведомлениям
    longpoll_server = LongpollServer()
    while True:
        # ждем событие
        updates = longpoll_server.get_update()
        if not updates:
            continue
        print(updates)
        # обрабатываем событие
        Handler(updates)
