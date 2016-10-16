import os

def getWorkDir():
    return os.getcwd()

def setWordDir(newPath):
    os.chdir(newPath)
    print("\nNew working directory: ", os.getcwd())
    return True
