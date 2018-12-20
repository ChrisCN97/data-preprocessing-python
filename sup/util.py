
import json
import base64

class ResultType:
	success = 0
	failed = 1

def result(type, desc = None, data = None, ext = None):
	'''
	# type 结果类型，如 ResultType.success
	# desc 描述
	# data 数据
	'''
	ret = { 'type': type }
	if desc:
		ret['desc'] = desc
	if data:
		ret['data'] = data
	if ext:
		ret['ext'] = ext
	return json.dumps(ret)

def bytes_to_b64(raw):
	'''
	# raw: bytes
	# return: string
	'''
	raw = base64.b64encode(raw) # b64 编码，产生 bytes
	return raw.decode('utf-8') # 解码，将数组转成字符串

# not used
# raw: string
# return: bytes
'''
def b64_to_bytes(raw):
	raw = raw.encode('utf-8') # 编码，将字符串转数组 
	return base64.b64decode(raw) # b64 解码，产生 bytes
'''