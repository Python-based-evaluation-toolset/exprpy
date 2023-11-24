#!/bin/python3

import os
import time

mock_result = "mock-result.txt"

if __name__ == "__main__":
    if os.path.isfile(mock_result):
        os.remove(mock_result)
