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

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 0)

# 设置工作目录
script_path = sys.path[0]
os.chdir(script_path)

eel.init("ui")

data = None
data_path = None
image = []

# pass
@eel.expose
def get_cwd():
	return os.getcwd()

# pass
# 查询目录子结构
@eel.expose
def open_path(p):
	ret = []
	for name in os.listdir(p):
		ret.append({
			'name': name,
			'type': 'dir' if path.isdir(path.join(p, name)) else 'file'
		})
	return json.dumps(ret)

# pass
# 读文件，获取数据，用于预览
@eel.expose
def get_data(p):
	global data
	global data_path
	data_path = p
	with open(p, 'rb') as f:
		data = pd.read_csv(f, ';')
		return data.to_json()

# pass
# 输出处理过的数据，到输入文件所在目录下
@eel.expose
def save_data():
	output_path = path.join(path.dirname(data_path), 'handled_' + path.basename(data_path))
	data.to_csv(output_path)
	return json.dumps({'output-path': output_path})

@eel.expose
def null_process(method):
	sup.null_process(data, method)
	return data.to_json()

@eel.expose
def noise_process(method):
	sup.noise_process(data, method)
	return data.to_json()

@eel.expose
def normalize(method):
	sup.normalize(data, method)
	return data.to_json()

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