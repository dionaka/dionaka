import os
from time import sleep
os.rmdir("ostry/rid")
sleep(2)
os.mkdir("ostry/rid")
print(os.path.isfile("ostry/rid"))
print(os.path.isdir("ostry/rid"))
if(os.path.exists("ostry/try1.txt")):
    os.remove("ostry/try1.txt")
print(os.listdir("ostry"))
