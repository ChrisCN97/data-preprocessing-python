'''
author: 李经纬
'''

import os
import sys
import eel

# 设置工作目录
script_path = sys.path[0]
os.chdir(script_path)

from main.context import Context

ctx = Context()

@eel.expose
def enable_mpc():
	return ctx.enable_mpc()

@eel.expose
def get_ncpus():
	return ctx.get_ncpus()

@eel.expose
def disable_mpc():
	return ctx.disable_mpc()

# pass
@eel.expose
def get_cwd():
	return ctx.get_cwd()

# pass
@eel.expose
def open_path(p):
	return ctx.open_path(p)

# pass
@eel.expose
def read_file(p):
	return ctx.read_file(p)
			
# pass
@eel.expose
def get_data():
	return ctx.get_data()

# not used
@eel.expose
def del_image(mid):
	return ctx.del_image(mid)

# pass
@eel.expose
def save_data():
	return ctx.save_data()

@eel.expose
def null_process(method, label=None):
	return ctx.null_process(method, label)

@eel.expose
def noise_process(method, label=None):
	return ctx.noise_process(method, label)

@eel.expose
def normalize(method, label=None):
	return ctx.normalize(method, label)

@eel.expose
def visualization(method, label):
	return ctx.visualization(method, label)

eel.init("ui")
eel.start("index.html", options={
	'port': 47932,
})