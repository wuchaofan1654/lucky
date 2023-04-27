# coding=utf-8
"""
# Create by wuchaofan 
# At 2023/4/11
# Current Dir 
"""
import time

from system.tasks import websocket_push


def test() -> None:
    for _ in range(10000):
        websocket_push(1, message='sent by python scripts~')
        time.sleep(0.5)


if __name__ == '__main__':
    test()
