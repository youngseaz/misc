
import os
#import pandas as pd
#import idautils
#import idaapi
try:
    # if user didn't set HOME environment variable, it will raise exception
    HOME = os.environ["HOME"]
except:
    HOME = os.path.expanduser("~")
DST_DIR = os.path.join(HOME, "searchunsafefunctions")

def get_unsafe_funcs():
    current_dir = os.path.dirname(__file__)
    file = os.path.join(current_dir, "unsafe_functions.txt")
    functions = []
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            functions.append(line.strip())
    return tuple(functions)
        

class Excel(object):
    def __init__(self):
        pass

    def create(self):
        pass


class UnsafeFuncFinder(object):
    def __init__(self):
        pass

    def find(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
    d = get_unsafe_funcs()
    print d


