# coding=utf-8
"""
# Create by wuchaofan 
# At 2023/4/7
# Current Dir custom
"""


import signal


def mitmproxy_flow_callback(request_meta):
    print(f"caught a flow ~ {request_meta}")


def handle_signal():
    signal.signal(signal.SIGINT, mitmproxy_flow_callback)


if __name__ == '__main__':
    handle_signal()
