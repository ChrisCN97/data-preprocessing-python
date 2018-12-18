'''
author: 李经纬
'''

import os
import sys
import pandas as pd

# 设置工作目录
script_path = sys.path[0]
os.chdir(script_path)

import eel
import sup
from util import df_slice

data = sup.read_file('test/test-data/bank.csv')
image = []

@eel.expose
def get_data():
    for piece in df_slice.cut(data):
        return piece

@eel.expose
def null_process(method):
    sup.null_process(data, method)

@eel.expose
def noise_process(method):
    sup.noise_process(data, method)

@eel.expose
def normalize(method):
    sup.normalize(data, method)

@eel.expose
def draw_line():
    sup.draw_line(None, data)

@eel.expose
def draw_bar():
    sup.draw_bar(None, data)

@eel.expose
def draw_pie():
    sup.draw_pie(None, data)

eel.init("ui")
eel.start("index.html")