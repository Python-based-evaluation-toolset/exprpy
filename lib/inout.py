import socket
import os


class IO:
    """
    IO is used to drive data flow of experience.

    This is a wrapper to construct experience by
    dictionary based configuration.
    """

    def __init__(self, sock_path: str):
        self.sock_path = sock_path

    def __send(self, msg):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            client.connect(self.sock_path)
            client.sendall(msg.encode())
        except Exception as e:
            raise Exception(f"Could not send request [msg: {msg}] with err: {e}")
        finally:
            client.close()

    def __cmd_build(self, type, name, args: dict):
        args_str = ""
        for k, v in args.items():
            if isinstance(v, list):
                for sub_v in v:
                    args_str += f" --{k} '{v}'"
            else:
                args_str += f" --{k} '{v}'"
        return f"{type.upper()} {name} {args_str}"

    def log_set(self, path):
        self.__send(f"IO PATH {path}")

    def log_append_set(self, boolean: bool):
        self.__send(f"IO APPEND {boolean}")

    def test(self, name, args: dict):
        self.__send(self.__cmd_build("TEST", name, args))

    def monitor(self, name, args: dict):
        self.__send(self.__cmd_build("MONITOR", name, args))

    def env(self, name, args: dict):
        self.__send(self.__cmd_build("ENV", name, args))

    def stop(self):
        self.__send("STOP CONTROLLER")
