from .unix_server import UnixServer
from .pubsub import Subscriber, FileSubscriber
import socket
import os
import sys
import signal
import select
import time


class Controller:
    """
    Controller is responsible to spawn another objects.
    This class acts as unix socket server.
    """

    def __init__(
        self,
        sock_path,
        test_path,
        monitor_path,
        env_path,
    ):
        # signal
        self.sign_chld = signal.getsignal(signal.SIGCHLD)

        # execution path
        self.test_home = test_path
        self.monitor_home = monitor_path
        self.env_home = env_path

        # IO flow
        self.file = None
        self.subscribers = []

        # unix socket generation
        try:
            os.unlink(sock_path)
        except OSError:
            if os.path.exists(sock_path):
                raise

        try:
            self.sock = socket.socket(
                socket.AF_UNIX,
                socket.SOCK_STREAM,
            )
            self.sock.bind(sock_path)
            self.sock.listen(10)  # listen up to 10 users
            self.server = UnixServer(self.sock)
        except Exception as e:
            print("Could not generate socket server:")
            raise e

    def __cmd_build(self, cmd):
        return ["/bin/bash", "-c", cmd]

    def __exception_ignore(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            pass

    def __exec_child(self, cmd):
        self.sock.close()
        pid, fd = os.forkpty()
        if pid == 0:
            cmd = self.__cmd_build(cmd)
            os.execvp(cmd[0], cmd)

        # os.set_blocking(fd, False)
        while True:
            try:
                readable, writable, exceptional = select.select([fd], [], [fd], 3)
                if fd in readable or fd in exceptional:
                    data = os.read(fd, 1024).decode()
                    # TODO: current subscriber inform mechanism is slow.
                    for sub in self.subscribers:
                        sub.recv(data)
                else:
                    # valid fork child still run
                    ret = os.waitpid(pid, os.WNOHANG)
                    time.sleep(0.1)  # wait for signal deliver
            except Exception as e:
                break

        self.subscribers.clear()
        sys.exit()

    def __zombie_killer_register(self):
        # clean zombie fork when it's done job
        def zombie_killer(sig, frame):
            os.wait()

        signal.signal(signal.SIGCHLD, zombie_killer)

    def __exec(self, cmd):
        pid = os.fork()

        if pid < 0:
            raise Exception("Could not fork to execute cmd in Controller.")
        elif pid == 0:
            signal.signal(signal.SIGCHLD, self.sign_chld)
            self.__exec_child(cmd)

    def test_spawn(self, cmd, args=""):
        self.__exec(f"{self.test_home}/{cmd} {args}")

    def monitor_spawn(self, cmd, args=""):
        self.__exec(f"{self.monitor_home}/{cmd} {args}")

    def env_spawn(self, cmd, args=""):
        self.__exec(f"{self.env_home}/{cmd} {args}")

    def subscriber_add(self, sub: Subscriber):
        self.subscribers.append(sub)

    def server_run(self):
        # start server
        self.__zombie_killer_register()
        while self.server.conn_wait():
            type, cmd, args = self.server.command_get_close()
            if type == "TEST":
                self.test_spawn(cmd, args)
            elif type == "MONITOR":
                self.monitor_spawn(cmd, args)
            elif type == "ENV":
                self.env_spawn(cmd, args)
            elif type == "IO":
                if self.file is None:
                    self.file = FileSubscriber()
                    self.subscribers.append(self.file)
                if cmd == "PATH":
                    self.file.log_set(args)
                elif cmd == "APPEND":
                    self.file.log_append(bool(args))
                else:
                    raise Exception(f"IO command is invalid: {cmd} {args}")
            elif type == "STOP" and cmd == "CONTROLLER":
                self.sock.close()
                break
            else:
                print(f"Error: type({type}) is not recognized")
