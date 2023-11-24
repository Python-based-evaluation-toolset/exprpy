#!/bin/python3

import time
import socket
import os

mock_sock = "/tmp/hieplnc"
mock_monitor = "monitor.py"


def client_send(msg):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(mock_sock)
        client.sendall(msg)
    except Exception as e:
        print(f"Error to open connection to controller: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    my_pid = os.getpid()
    monitor_cmd = f"MONITOR {mock_monitor} --pid {my_pid}"
    client_send(str.encode(monitor_cmd))
    for i in range(10):
        print(f"Loop circle [pid: {my_pid}]: {i}")
        time.sleep(0.5)
