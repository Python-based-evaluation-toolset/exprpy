import socket
import os


class IO:
    """
    IO is used to drive data flow of experience.

    This is a wrapper to construct experience by
    dictionary based configuration.
    """

    def __init__(self, sock_path: str):
        self.output = None
        self.log_append = ""
        self.sock_path = sock_path

    def __send(self, msg):
        if self.output is not None and not msg.startswith("STOP"):
            msg = f"{msg} 2>&1 | tee {self.log_append} {self.output}"
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            client.connect(self.sock_path)
            client.sendall(msg.encode())
        except Exception as e:
            raise Exception(f"Could not send request [msg: {msg}] with err: {e}")
        finally:
            client.close()

    def __cmd_build(self, type, name, args: dict):
        args_str = " ".join([f"--{k} {v}" for k, v in args.items()])
        return f"{type.upper()} {name} {args_str}"

    def output_set(self, path):
        self.output = path

    def log_append_set(self, boolean: bool):
        self.log_append = "-a" if boolean else ""

    def test(self, name, args: dict):
        self.__send(self.__cmd_build("TEST", name, args))

    def monitor(self, name, args: dict):
        self.__send(self.__cmd_build("MONITOR", name, args))

    def env(self, name, args: dict):
        self.__send(self.__cmd_build("ENV", name, args))

    def stop(self):
        self.__send("STOP CONTROLLER")
