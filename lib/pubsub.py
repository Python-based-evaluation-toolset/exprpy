class Subscriber:
    """
    Base subscriber object to communicate
    with controller log driven mechanism.
    """

    def __init__(self):
        pass

    def __recv(self, msg):
        """
        This method is used by controller
        to stream test log.
        """
        pass


# TODO: implement file saving subscriber
class FileSubscriber:
    pass
