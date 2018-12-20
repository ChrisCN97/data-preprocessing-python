# data-preprocessing-python
数据预处理

[接口定义](doc/接口定义.md)

# 模块说明

## sup

主要功能模块

### dataIO

IO工具模块

### data_normalization

数据规范化

- min-max
- z-score
- 小数标定

### noise_processing

去噪

- 平均值
- 边界值
- 中值

### null_processing

空值处理

- 均值
- 均值-方差
- 正态随机

### util

* result: 返回 json 的工具函数
* bytes_to_b64: 二进制流转  base64 编码

### visualization

可视化

- 条形图
- 折线图
- 饼图

# app.py

* 使用```Context```保存操作数据、可视化图像、操作记录
* 通过 eel 使用```@eel.expose``暴露接口给前端
* 启动 eel