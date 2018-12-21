
import os
import json
import base64
import shutil
import traceback
from os import path
import pandas as pd
from .pp_sup import MPCompute

# pandas 配置
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 0)


import sup
from sup.util import bytes_to_b64, ResultType, result

# 映射 method 参数为操作类型
null_type = {0: '均值', 1: '均值-方差', 2: '正态随机'}
noise_type = {0: '平均值', 1: '边界值', 2: '中值'}
normalize_type = {0: 'min-max', 1: 'z-score', 2: '小数标定'}

class Context(object):
    max_rows = 500
    def __init__(self):
        self.__reset()
        self.data = None
        self.data_path = None
        self.mpc = None # MPCompute()

    def __reset(self):
        self.images = {}
        self.op_records = []
        self.data_version = 0
        self.image_count = 0

    def __new_version(self, data, op_type):
        '''
        data: 新版本数据
        op_type: 操作类型，代表本次更新数据使用的操作
        数据更新后 data_version 自增
        '''
        self.data = data
        self.data_version += 1
        self.op_records.append(op_type)
	
    def __get_data(self):
        '''
        返回 data 用于前端预览，如果 data 行数过多会进行裁剪
        '''
        ret = { 'nr': 0, 'nc': 0, 'data': None }
        if (not self.data is None) and (not self.data.empty):
            ret['nr'], ret['nc'] = self.data.shape
            if ret['nr'] > Context.max_rows:
                ret['data'] = self.data[0:Context.max_rows].to_json()
            else:
                ret['data'] = self.data.to_json()
        return json.dumps(ret)

    def __add_image(self, type, label, data):
        '''
        # type: 图像内容——直方图、折线图、饼图
        # data: 图像 bytes 数据
        # return: image ID，格式: data_version.image_count.label.bar，实例: 1.3.age.line
        '''
        i = '%d-%d-%s-%s' % (self.data_version, self.image_count, label, type)
        self.image_count += 1
        self.images[i] = data
        return i
	
    def __del_image(self, mid):
        '''
        删除图像缓存
        '''
        if mid in self.images:
            del self.images[mid]
            return True
        return False
    
    # 接口

    def enable_mpc(self):
        '''
        启用mpc
        '''
        try:
            self.mpc = MPCompute()
            return result(ResultType.success)
        except:
            msg = traceback.format_exc()
            return result(ResultType.failed, desc=msg)
    
    def get_ncpus(self):
        '''
        获取可用核数
        '''
        if self.mpc:
            return result(ResultType.success, data=self.mpc.ncpus)
        else:
            return result(ResultType.failed, desc='multiple cores compute is disable')

    def disable_mpc(self):
        '''
        禁用mpc
        '''
        try:
            self.mpc.shutdown()
            self.mpc = None
            return result(ResultType.success)
        except:
            msg = traceback.format_exc()
            return result(ResultType.failed, desc=msg)
            
    def get_cwd(self):
        '''
        获取工作路径
        '''
        return result(ResultType.success, data=os.getcwd())
        
    def open_path(self, p):
        '''
        查询目录子结构
        '''
        data = []
        for name in os.listdir(p):
            data.append({
                'name': name,
                'type': 'dir' if path.isdir(path.join(p, name)) else 'file'
            })
        return result(ResultType.success, data=data)

    '''
    html格式输出再输入内容又增加！也就是说html输出的数据不能读入后直接使用
    '''
    sup_file_type = ['csv', 'json', 'html'] # excel feather, gbq, hdf, msgpack, parquet, pickle, sql, stata

    def read_file(self, p):
        '''
        读文件，获取数据，用于预览
        支持的数据文件类型：sup_file_type
        '''
        name = path.basename(p)
        i = name.rfind('.')
        file_type = name[i + 1:].lower() if i >= 0 else None
        self.data_path = p
        with open(p, 'rb') as f:
            if file_type and file_type in Context.sup_file_type:
                try:
                    if file_type == 'csv':
                        self.data = pd.read_csv(f, ';')
                    else:
                        self.data = getattr(pd, 'read_' + file_type)(f)
                    self.__reset()
                    return result(ResultType.success, data=self.__get_data())
                except:
                    msg = traceback.format_exc()
                    return result(ResultType.failed, desc=msg)
            else:
                return result(ResultType.failed, desc='unsupported file type: ' + file_type)
        return result(ResultType.failed, desc='cannot open file: ' + p)

    def get_data(self):
        '''
        返回 context 中保存的 data
        '''
        return result(ResultType.success, data=self.__get_data())
    
    def del_image(self, mid):
        '''
        从 ctx 中删除图片
        '''
        if self.__del_image(mid):
            return result(ResultType.success)
        return result(ResultType.failed, desc='invalid image id')

    def save_data(self):
        '''
        在输入目录下创建 DPTool-output，存储数据到该目录下
        '''
        try:
            output_dir = path.join(path.dirname(self.data_path), 'DPTool-output')
            if path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.mkdir(output_dir)
            # 存储处理后的数据
            output_path = path.join(output_dir, str(self.data_version) + '-' + path.basename(self.data_path))
            self.data.to_csv(output_path)
            # 存储视图
            for name in self.images:
                with open(path.join(output_dir, name + '.png'), 'wb') as f:
                    f.write(self.images[name])
            # 存储操作日志
            with open(path.join(output_dir, 'op-records.txt'), 'wb') as f:
                for item in self.op_records:
                    f.write((item + '\n').encode('utf-8'))
            return result(ResultType.success, data=output_dir)
        except:
            msg = traceback.format_exc()
            return result(ResultType.failed, desc=msg)

    def null_process(self, method):
        '''
        空值处理
        '''
        try:
            new_data = sup.null_process(self.data, method)
            self.__new_version(new_data, 'null process (%s)' % noise_type[method])
            return result(ResultType.success, data=self.__get_data())
        except:
            msg = traceback.format_exc()
            return result(ResultType.failed, desc=msg)
        
    def noise_process(self, method):
        '''
        噪声处理
        '''
        try:
            new_data = sup.noise_process(self.data, method)
            self.__new_version(new_data, 'noise process (%s)' % noise_type[method])
            return result(ResultType.success, data=self.__get_data())
        except:
            msg = traceback.format_exc()
            return result(ResultType.failed, desc=msg)
        
    def normalize(self, method):
        '''
        数据规范化
        '''
        try:
            new_data = sup.normalize(self.data, method)
            self.__new_version(new_data, 'normalize (%s)' % noise_type[method])
            return result(ResultType.success, data=self.__get_data())
        except:
            msg = traceback.format_exc()
            return result(ResultType.failed, desc=msg)
    
    def draw_line(self, label):
        '''
        绘制折线图
        '''
        try:
            data = sup.draw_line(label, self.data[label])
            i = self.__add_image('line', label, data)
            return result(ResultType.success, data=bytes_to_b64(data), ext=i)
        except:
            msg = traceback.format_exc()
            return result(ResultType.failed, desc=msg)

    def draw_bar(self, label):
        '''
        绘制直方图
        '''
        try:
            data = sup.draw_bar(label, self.data[label])
            i = self.__add_image('bar', label, data)
            return result(ResultType.success, data=bytes_to_b64(data), ext=i)
        except:
            msg = traceback.format_exc()
            return result(ResultType.failed, desc=msg)

    def draw_pie(self, label):
        '''
        绘制饼图
        '''
        try:
            data = sup.draw_pie(label, self.data[label])
            i = self.__add_image('pie', label, data)
            return result(ResultType.success, data=bytes_to_b64(data), ext=i)
        except:
            msg = traceback.format_exc()
            return result(ResultType.failed, desc=msg)