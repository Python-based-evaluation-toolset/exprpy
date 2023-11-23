class UnixServer:
    """
    Handle unix connection
    and convert IO text to command.
    """

    def __init__(self, socket):
        # internal meta
        self.conn = None
        self.text = None
        # connection
        if not socket:
            raise Exception("Socket is not valid.")
        self.sock = socket

    def conn_wait(self):
        self.conn, client_addr = self.sock.accept()
        return self.conn

    def conn_get(self):
        return self.conn

    def raw_get_close(self):
        try:
            buff = b""
            while True:
                data = self.conn.recv(1024)
                buff += data
                if not data:
                    break
            self.text = buff.decode()
        finally:
            self.conn.close()
            self.conn = None
            return self.text
