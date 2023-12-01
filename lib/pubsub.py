class Subscriber:
    """
    Base subscriber object to communicate
    with controller log driven mechanism.
    """

    def __init__(self):
        pass

    def recv(self, msg: str):
        """
        This method is used by controller
        to stream test log.
        """
        print(msg, end="")


class FileSubscriber(Subscriber):
    def __init__(self):
        super().__init__()
        self.path = None
        self.log = None
        self.append = False

    def __del__(self):
        self.__close_log()

    def __open_log(self):
        self.log = open(self.path, "a+" if self.append else "w+")

    def __close_log(self):
        if self.log is not None:
            self.log.close()
            self.log = None

    def log_set(self, path: str):
        self.path = path

    def log_append(self, boolean: bool):
        self.append = boolean

    def recv(self, msg: str):
        # Disable log if path is invalid
        if self.path is None or self.path == "":
            return
        if self.log is None:
            self.__open_log()
        self.log.write(msg)
        self.__close_log()
