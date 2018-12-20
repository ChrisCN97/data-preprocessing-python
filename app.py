'''
author: 李经纬
'''

import os
import sys
import json
import base64
import pandas as pd
from os import path

import eel
import sup
from sup.util import *

# pandas 配置
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 0)

# 设置工作目录
script_path = sys.path[0]
os.chdir(script_path)

class Context(object):
	max_rows = 500
	def __init__(self):
		self.data = None
		self.data_path = None
		self.images = {}
		self.imageId = 0
	
	def get_data(self):
		if self.data.shape[0] > Context.max_rows:
			return self.data[0:Context.max_rows].to_json()
		else:
			return self.data.to_json()

	def add_image(self, data):
		'''
		# data: 图像 bytes 数据
		# return: image ID
		'''
		i = self.imageId
		self.imageId += 1
		self.images[i] = data
		return i
	
	def del_image(self, mid):
		if mid in self.images:
			del self.images[mid]
			return True
		return False

ctx = Context()

# pass
# 获取工作路径
@eel.expose
def get_cwd():
	return result(ResultType.success, data=os.getcwd())

# pass
# 查询目录子结构
@eel.expose
def open_path(p):
	data = []
	for name in os.listdir(p):
		data.append({
			'name': name,
			'type': 'dir' if path.isdir(path.join(p, name)) else 'file'
		})
	return result(ResultType.success, data=data)

# pass
# 读文件，获取数据，用于预览
@eel.expose
def read_file(p):
	ctx.data_path = p
	with open(p, 'rb') as f:
		ctx.data = pd.read_csv(f, ';')
		return result(ResultType.success, data=ctx.get_data())
	return result(ResultType.failed, desc='cannot open file: ' + p)
			
# pass
# 返回 context 中保存的 data
@eel.expose
def get_data():
	return result(ResultType.success, data=ctx.get_data())

# pass
# 输出处理过的数据，到输入文件所在目录下
@eel.expose
def save_data():
	output_path = path.join(path.dirname(ctx.data_path), 'handled_' + path.basename(ctx.data_path))
	ctx.data.to_csv(output_path)
	return result(ResultType.success, data=output_path)

# 空值处理
@eel.expose
def null_process(method):
	sup.null_process(ctx.data, method)
	return result(ResultType.success, data=ctx.get_data())

# 噪声处理
@eel.expose
def noise_process(method):
	sup.noise_process(ctx.data, method)
	return result(ResultType.success, data=ctx.get_data())

# 数据规范化
@eel.expose
def normalize(method):
	sup.normalize(ctx.data, method)
	return result(ResultType.success, data=ctx.get_data())

# 绘制折线图
@eel.expose
def draw_line(label):
	data = sup.draw_line(label, ctx.data[label])
	i = ctx.add_image(data)
	return result(ResultType.success, data=bytes_to_b64(data), ext=i)

# pass
# 绘制直方图
@eel.expose
def draw_bar(label):
	data = sup.draw_bar(label, ctx.data[label])
	i = ctx.add_image(data)
	return result(ResultType.success, data=bytes_to_b64(data), ext=i)

# 绘制饼图
@eel.expose
def draw_pie(label):
	data = sup.draw_pie(label, ctx.data[label])
	i = ctx.add_image(data)
	return result(ResultType.success, data=bytes_to_b64(data), ext=i)

# 从 ctx 中删除图片
@eel.expose
def del_image(mid):
	if ctx.del_image(mid):
		return result(ResultType.success)
	return result(ResultType.failed, desc='invalid image id')

eel.init("ui")
eel.start("index.html", options={
	'port': 47932,
})