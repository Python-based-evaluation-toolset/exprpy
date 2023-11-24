#!/bin/python3

import time
import socket
import os
import sys

mock_sock = "/tmp/hieplnc"
mock_monitor = "monitor.py"


def client_send(msg):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(mock_sock)
        client.sendall(msg.encode())
    except Exception as e:
        raise Exception(f"Could not send request [msg: {msg}] with err: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    my_pid = os.getpid()
    client_send(f"MONITOR {mock_monitor} --pid {my_pid}")
    for i in range(10):
        print(f"Loop circle [pid: {my_pid}]: {i}")
        time.sleep(0.5)
