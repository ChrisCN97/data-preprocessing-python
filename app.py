'''
author: 李经纬
'''

import os
import sys
import json
import pandas as pd
from os import path

import eel
import sup

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 设置工作目录
script_path = sys.path[0]
os.chdir(script_path)

eel.init("ui")

data = None
image = []

def ret_val(success, data):
	return json.dumps({
		'success': success,
		'data': str(data)
	})

# 实测通过
@eel.expose
def get_cwd():
	return os.getcwd()

# 实测通过
@eel.expose
def open_path(p):
	ret = []
	for name in os.listdir(p):
		ret.append({
			'name': name,
			'type': 'dir' if path.isdir(path.join(p, name)) else 'file'
		})
	return json.dumps(ret)

# 实测通过
@eel.expose
def get_data(p):
	with open(p, 'rb') as f:
		reader = pd.read_csv(f, iterator=True)
		chunks = []
		for chunk in reader:
			chunks.append(chunk)
		data = pd.concat(chunks, ignore_index=True)
		return ret_val(True, data)

@eel.expose
def null_process(method):
	sup.null_process(data, method)
	return ret_val(True, data)

@eel.expose
def noise_process(method):
	sup.noise_process(data, method)
	return ret_val(True, data)

@eel.expose
def normalize(method):
	sup.normalize(data, method)
	return ret_val(True, data)

@eel.expose
def draw_line():
	# 从 plt 获取图像二进制流，传给前端，并保存到 image，如果 data 更新了，清空 image
    plt = sup.draw_line(None, data)

@eel.expose
def draw_bar():
    plt = sup.draw_bar(None, data)

@eel.expose
def draw_pie():
    plt = sup.draw_pie(None, data)

eel_options = {
	'port': 47932,
	# 'chromeFlags': ['--kiosk']
}
eel.start("index.html", options=eel_options)