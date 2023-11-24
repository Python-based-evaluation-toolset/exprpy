#!/bin/python3

import time
import socket
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from lib.inout import IO

mock_sock = "/tmp/hieplnc"
mock_result = "mock-result.txt"
mock_monitor = "monitor.py"

if __name__ == "__main__":
    print(os.getcwd())
    my_pid = os.getpid()
    client = IO(mock_sock)
    client.output_set(mock_result)
    client.log_append_set(True)
    client.monitor(mock_monitor, {"pid": my_pid})
    for i in range(10):
        print(f"Loop circle [pid: {my_pid}]: {i}")
        time.sleep(0.5)
