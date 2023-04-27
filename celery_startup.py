from multiprocessing import Process
import logging
import os
import time

logger = logging.getLogger('startup')


class CeleryStartup(object):
    @classmethod
    def _start_celery_worker(cls):
        time.sleep(3)
        os.system("celery -A application worker -l info")
        logger.info(f'正在启动 celery worker 服务～')

    @classmethod
    def _start_celery_beat(cls):
        time.sleep(3)
        os.system("celery -A application beat -l info")
        logger.info(f'正在启动 celery beat 服务～')

    @classmethod
    def _start_celery_flower(cls):
        time.sleep(3)
        os.system("celery -A application flower")
        logger.info(f'正在启动 celery flower 服务～')

    def __new__(cls, *args, **kwargs):
        processes = [
            Process(target=cls._start_celery_worker),
            Process(target=cls._start_celery_beat),
            Process(target=cls._start_celery_flower)
        ]
        [process.start() for process in processes]
        [process.join() for process in processes]

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("celery服务已关闭～")


if __name__ == '__main__':
    CeleryStartup()
