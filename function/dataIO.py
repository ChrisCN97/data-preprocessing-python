"""
# 接口1.1、1.2、1.3、1.4
# 读取文件，预览文件，选择属性列，判断类型，保存文件
# made by 崔楠，2018.12.17
"""

import pandas as pd

# 读取文件
def read_file(openPath):
    try:
        data = pd.read_csv(openPath)
    except FileNotFoundError:
        print("文件不存在！")
        return False
    except:
        print("未知错误！")
        return False
    else:
        print("文件加载成功！")
        return data

# 文件预览信息
def file_skim(data):
    skimInfo = data.head(3).to_string()
    skimInfo += "\n...... ......\n"
    skimInfo += "\n".join(data.tail(3).to_string().split("\n")[1:])
    props = data.columns.tolist()
    return skimInfo, props

# 选择属性列，判断数据类型
def choose_property(data, property):
    if str(data[property].dtype) == "object":
        return "文本"
    else:
        return "数值"

# 保存文件
def save(data, savaPath):
    try:
        data.to_csv(savaPath)
    except:
        print("保存失败！")
        return False
    else:
        print("保存成功！")