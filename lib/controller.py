from .unix_server import UnixServer
import socket
import subprocess
import os
import sys


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
        # execution path
        self.test_home = test_path
        self.monitor_home = monitor_path
        self.env_home = env_path

        # IO flow
        self.log_path = None
        self.log_append = ""

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
        if self.log_path is not None and len(self.log_path) > 0:
            return f"{cmd} 2>&1 | tee {self.log_append} {self.log_path}"
        else:
            return cmd

    def __exec(self, cmd):
        pid = os.fork()
        if pid < 0:
            raise Exception("Could not fork to execute cmd in Controller.")
        elif pid == 0:
            self.sock.close()
            subprocess.run(self.__cmd_build(cmd), shell=True)
            sys.exit()

    def test_spawn(self, cmd, args=""):
        self.__exec(f"{self.test_home}/{cmd} {args}")

    def monitor_spawn(self, cmd, args=""):
        self.__exec(f"{self.monitor_home}/{cmd} {args}")

    def env_spawn(self, cmd, args=""):
        self.__exec(f"{self.env_home}/{cmd} {args}")

    def server_run(self):
        while self.server.conn_wait():
            type, cmd, args = self.server.command_get_close()
            if type == "TEST":
                self.test_spawn(cmd, args)
            elif type == "MONITOR":
                self.monitor_spawn(cmd, args)
            elif type == "ENV":
                self.env_spawn(cmd, args)
            elif type == "IO":
                if cmd == "PATH":
                    self.log_path = args
                elif cmd == "APPEND":
                    self.log_append = "-a" if bool(args) else ""
                else:
                    raise Exception(f"IO command is wrong: {cmd} {args}")
            elif type == "STOP" and cmd == "CONTROLLER":
                self.sock.close()
                break
            else:
                print(f"Error: type({type}) is not recognized")
