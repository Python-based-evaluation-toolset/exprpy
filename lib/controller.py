import subprocess


class Controller:
    """
    Controller is responsible to spawn another objects.
    """

    def __init__(self, test_path, monitor_path, env_path):
        self.test_home = test_path
        self.monitor_home = monitor_path
        self.env_home = env_path

    def __exec(self, cmd):
        subprocess.run(cmd, shell=True)

    def test_spawn(self, cmd):
        self.__exec(f"{self.test_home}/{cmd}")

    def monitor_spawn(self, cmd):
        self.__exec(f"{self.monitor_home}/{cmd}")

    def env_spawn(self, cmd):
        self.__exec(f"{self.env_home}/{cmd}")
