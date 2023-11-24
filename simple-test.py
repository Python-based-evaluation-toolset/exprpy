from lib.controller import Controller
from lib.inout import IO
import os
import time
import sys
import socket
import signal

if __name__ == "__main__":
    mock_sock = "/tmp/hieplnc"
    mock_result = "mock-result.txt"
    mock_arg = {
        "sock_path": mock_sock,
        "test_path": "./test",
        "monitor_path": "./test",
        "env_path": "./test",
    }

    # client interface
    client = IO(mock_sock)

    # child - controller process
    pid = os.fork()
    if pid < 0:
        raise Exeception("Could not fork test to controller process.")
    elif pid == 0:
        control = Controller(**mock_arg)
        control.server_run()
        sys.exit()
    else:
        time.sleep(1)  # wait for controller

    # log configuration
    client.log_set(mock_result)
    client.log_append_set(True)

    print("#----- ENV CLEAN -----#")
    print("[DEMO] Command: ENV env.py")
    client.env("env.py", {})
    time.sleep(1)

    print("#----- SIMPLE TEST -----#")
    print("[DEMO] Command: TEST loop-20.py")
    client.test("loop-20.py", {})
    time.sleep(3)

    print("#----- SELF-AWARE TEST -----#")
    client.test("loop-10-self-monitor.py", {})
    time.sleep(6)

    print("[DEMO] Command: STOP CONTROLLER")
    client.stop()

    # Wait for controller to die
    os.wait()
