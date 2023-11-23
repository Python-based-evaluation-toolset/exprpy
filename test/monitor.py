#!/bin/python3

import argparse
import os
import time

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pid", help="target process pid", required=True)
arg = parser.parse_args()
pid = arg.pid

if __name__ == "__main__":
    path = f"/proc/{pid}"
    print("Monitor start.")
    while os.path.isdir(path):
        print("Process is existed.")
        time.sleep(1)
    print("Monitor end.")
