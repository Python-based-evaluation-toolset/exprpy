from .unix_server import UnixServer
import subprocess
import socket
import os


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
        self.test_home = test_path
        self.monitor_home = monitor_path
        self.env_home = env_path

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

    def __exec(self, cmd):
        subprocess.run(cmd, shell=True)

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
            elif type == "STOP" and cmd == "CONTROLLER":
                self.sock.close()
                break
            else:
                print(f"Error: type({type}) is not recognized")
