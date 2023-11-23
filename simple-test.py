from lib.controller import Controller
import os
import time
import sys
import socket
import signal


def client_send(mock_sock, msg):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(mock_sock)
        client.sendall(msg)
    except Exception as e:
        print(f"Error to open connection to controller: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    mock_sock = "/tmp/hieplnc"
    mock_arg = {
        "sock_path": mock_sock,
        "test_path": "./test",
        "monitor_path": "./test",
        "env_path": "./test",
    }

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

    print("[DEMO] Command: TEST loop-20.py")
    client_send(mock_sock, b"TEST loop-20.py")
    time.sleep(2)
    print("[DEMO] Command: STOP CONTROLLER")
    client_send(mock_sock, b"STOP CONTROLLER")

    # Wait for controller to die
    os.wait()
