import os

from application.settings import BASE_DIR

from celery import shared_task
import logging
from application.celery import app
from system.tasks import websocket_push


logger = logging.getLogger('django')


@shared_task
def start_mitmproxy_task(listen_port=9999):
    try:
        filepath = os.path.join(BASE_DIR, 'custom', 'utils', 'addons.py')
        os.system(f'mitmproxy -s {filepath} -p {listen_port}')
        return "mitm启动成功～"
    except Exception as error:
        return f"mitm服务启动异常：{error}"


@shared_task
def shutdown_mitmproxy_task(listen_port):
    result = os.popen(f"lsof -i:{listen_port} | grep LISTEN").read()
    pid = [ele for ele in result.split(' ') if ele][1]
    os.popen(f'kill -9 {pid}')
    logger.info(f"mitmproxy {listen_port} =》服务已关闭～")
    return f"mitm服务已关闭～"


@shared_task
def check_mitmproxy_status_task(listen_port=9999):
    """
    定时检查mitmproxy状态是否开启
    :return:
    """
    result = os.popen(f"lsof -i:{listen_port} | grep LISTEN").read()
    if not result:
        result = start_mitmproxy_task.delay()
        return result

    return 'mitm服务正常～'


@app.task
def receive_push_recording_task(user_id, message):
    """开启任务将recording记录，通过websocket推送给指定用户"""
    websocket_push(
        user_id=user_id,
        message={
            "sender": 'system',
            "contentType": 'TEXT',
            "content": f"{message}",
        })


@app.task
def disconnect_push_recording_task(user_id, message):
    """中断推送recording任务"""
    result = receive_push_recording_task(user_id, message)
    print(result)
