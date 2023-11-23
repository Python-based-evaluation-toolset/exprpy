from lib.controller import Controller

if __name__ == "__main__":
    mock_arg = {
        "test_path": "./test",
        "monitor_path": "./test",
        "env_path": "./test",
    }
    control = Controller(**mock_arg)
    control.test_spawn("loop-20.py")
