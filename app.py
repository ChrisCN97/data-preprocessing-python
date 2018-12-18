'''
author: 李经纬
'''

import os
import sys

# 设置工作目录
script_path = sys.path[0]
os.chdir(script_path)

# from function import *
import eel

eel.init("ui")

@eel.expose
def hello():
    return "hello"

eel.start("index.html")