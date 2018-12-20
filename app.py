'''
author: 李经纬
'''

import os
import sys
import json
import base64
import shutil
import traceback
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
		self.op_records = []
		self.data_version = 0
		self.image_count = 0

	def new_version(self, op_type):
		'''
		op_type: 操作类型
		'''
		self.op_records.append(op_type)
		self.data_version += 1
	
	def get_data(self):
		if self.data.shape[0] > Context.max_rows:
			return self.data[0:Context.max_rows].to_json()
		else:
			return self.data.to_json()

	def add_image(self, type, data):
		'''
		# type: 图像内容——直方图、折线图、饼图
		# data: 图像 bytes 数据
		# return: image ID
		'''
		i = str(self.data_version) + '.' + str(self.image_count) + '.' + type
		self.image_count += 1
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

# not used
# 从 ctx 中删除图片
@eel.expose
def del_image(mid):
	if ctx.del_image(mid):
		return result(ResultType.success)
	return result(ResultType.failed, desc='invalid image id')

# pass
@eel.expose
def save_data():
	output_dir = path.join(path.dirname(ctx.data_path), 'DPTool-output')
	if path.exists(output_dir):
		shutil.rmtree(output_dir)
	os.mkdir(output_dir)
	# 存储处理后的数据
	output_path = path.join(output_dir, str(ctx.data_version) + '.' + path.basename(ctx.data_path))
	ctx.data.to_csv(output_path)
	# 存储视图
	for name in ctx.images:
		with open(path.join(output_dir, name + '.png'), 'wb') as f:
			f.write(ctx.images[name])
	# 存储操作日志
	with open(path.join(output_dir, 'op.records'), 'wb') as f:
		for item in ctx.op_records:
			f.write(item)
			f.write('\n')
	# return
	return result(ResultType.success, data=output_dir)

null_type = {0: '均值', 1: '均值-方差', 2: '正太随机'}
noise_type = {0: '平均值', 1: '边界值', 3: '中值'}
normalize_type = {0: 'min-max', 1: 'z-score', 2: '小数标定'}

# 空值处理
@eel.expose
def null_process(method):
	try:
		sup.null_process(ctx.data, method)
		ctx.new_version('null process - ' + null_type[method])
		return result(ResultType.success, data=ctx.get_data())
	except:
		msg = traceback.format_exc()
		return result(ResultType.failed, desc=msg)

# 噪声处理
@eel.expose
def noise_process(method):
	try:
		sup.noise_process(ctx.data, method)
		ctx.new_version('noise process - ' + noise_type[method])
		return result(ResultType.success, data=ctx.get_data())
	except:
		msg = traceback.format_exc()
		return result(ResultType.failed, desc=msg)

# 数据规范化
@eel.expose
def normalize(method):
	try:
		sup.normalize(ctx.data, method)
		ctx.new_version('normalize - ' + normalize_type[method])
		return result(ResultType.success, data=ctx.get_data())
	except:
		msg = traceback.format_exc()
		return result(ResultType.failed, desc=msg)

# pass
# 绘制折线图
@eel.expose
def draw_line(label):
	try:
		data = sup.draw_line(label, ctx.data[label])
		i = ctx.add_image('line', data)
		return result(ResultType.success, data=bytes_to_b64(data), ext=i)
	except:
		msg = traceback.format_exc()
		return result(ResultType.failed, desc=msg)

# pass
# 绘制直方图
@eel.expose
def draw_bar(label):
	try:
		data = sup.draw_bar(label, ctx.data[label])
		i = ctx.add_image('bar', data)
		return result(ResultType.success, data=bytes_to_b64(data), ext=i)
	except:
		msg = traceback.format_exc()
		return result(ResultType.failed, desc=msg)

# pass
# 绘制饼图
@eel.expose
def draw_pie(label):
	try:
		data = sup.draw_pie(label, ctx.data[label])
		i = ctx.add_image('pie', data)
		return result(ResultType.success, data=bytes_to_b64(data), ext=i)
	except:
		msg = traceback.format_exc()
		return result(ResultType.failed, desc=msg)

eel.init("ui")
eel.start("index.html", options={
	'port': 47932,
})