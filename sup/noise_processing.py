import pandas as pd
import numpy as np

'''
# 数据噪声处理（平均值去噪、边界值去噪、中值去噪）
# made by 张晋豪, 2018.12.18
'''


# 去噪处理函数（noise_process），data为输入的原始dataframe, method参数不同取值
# 0：平均值
# 1：边界值
# 2：中值
def noise_process(data, method, label=None):
    data_copy = data.copy()
    if (label != None):
        data = pd.DataFrame({label: data[label].values})
    l = data.columns.tolist()
    str_list = []
    number_list = []
    for i in l:
        if (isinstance(data.iloc[1][i], str) == True):
            str_list.append(i)
        else:
            number_list.append(i)
    # print("str_list " + str(str_list))
    # print("number_list " + str(number_list))

    data_str = data[str_list]
    data = data[number_list]

    row = data.shape[0]  # 行
    col = data.shape[1]  # 列
    list = data.columns.values.tolist()  # 属性列表
    array = data.astype(float).values  # numpy数组

    array_copy = array.copy()  # 获取输入dataframe的原始备份，用作中间计算处理
    array_copy2 = array.copy()  # 获取输入dataframe的原始备份，用作结果返回矩阵
    array_rank = np.array(np.zeros(row * col)).reshape(row, col)  # 按列排序后到排序前的映射
    array2rank = np.array(np.zeros(row * col)).reshape(row, col)  # 按列排序前到排序后的映射
    for i in range(col):
        array_rank[:] = array_copy.argsort(0)  # 排序后的数组该位置对应原始数组的位置
        array.sort(0)  # 按列排序

    # array已排序
    # array_copy为原始数组
    # array_rank排序后到排序前
    # array2rank排序前到排序后

    for i in range(row):
        for j in range(col):
            # 根据按列排序后的，对应着排序前下标的矩阵rank_rank中值的行坐标
            # 即对应着原始矩阵位置的矩阵单元
            # 设置列排序前到排序后的映射的矩阵array_rank2的单元为其横坐标
            # 由于是按列排序，所以列坐标不变
            array2rank[int(array_rank[i, j]), j] = i

    # 两个恒等式
    # 排序后的矩阵[i,j]=原始矩阵[列排序后到排序前的映射[i,j],j]
    # array[i, j] == array_copy[int(array_rank[i, j]), j] 为真
    # 原始矩阵[i,j]=排序后的矩阵[列排序前到排序后的映射[i,j],j]
    # array_copy[i, j] ==  array[int(array2rank[i, j]), j] 为真

    if method == 0:  # 0：平均值
        # 分箱操作正式开始，以1/10为单位进行分箱
        count = 0  # 单项计数器
        k = 0  # 十分之一模块数计数器
        for i in range(row):
            start = int(k / 10.0 * row)  # 单位起点
            end = int((k + 1) / 10.0 * row)  # 单位终点
            List = array_rank[start:end].astype(int)  # 将这一区间内的排序结果转换为int类型
            for j in range(col):
                mean = np.sum(array_copy[List, j]) / (1 / 10.0 * row)  # 计算区间均值
                array_copy2[int(array_rank[i, j]), j] = mean  # 原始矩阵的备份[排序前对应排序位置]=均值
            count += 1
            if (count % (row / 10) == 0):
                k += 1

    elif method == 1:  # 1：边界值
        # 分箱操作正式开始，以1/10为单位进行分箱
        count = 0  # 单项计数器
        k = 0  # 十分之一单位计数器
        for i in range(row):  # 对每一行
            start = int(k / 10.0 * row)  # 单位起点
            end = int((k + 1) / 10.0 * row) - 1  # 单位终点
            for j in range(col):  # 对每一列
                up = array_copy2[end, j]  # 取排序后的上限
                array_copy2[int(array_rank[i, j]), j] = up  # 取区间上限降噪
            count += 1
            if (count % (row / 10) == 0):
                k += 1

    elif method == 2:  # 2：中值
        count = 0  # 单项计数器
        k = 0  # 十分之一累积计数器
        for i in range(row):  # 每一行
            start = int(k / 10.0 * row)  # 十分之一起始位置
            end = int((k + 1) / 10.0 * row) - 1  # 十分之一结束位置
            for j in range(col):
                Middle = array_copy2[int((start + end) / 2), j]  # 寻找中值
                array_copy2[int(array_rank[i, j]), j] = Middle  # 用中值降噪
            count += 1
            if (count % (row / 10) == 0):
                k += 1

    # array_copy2 = pd.merge(array_copy2, data_str)
    normal_df = pd.DataFrame(array_copy2, index=range(row), columns=list)
    # normal_df = pd.concat([normal_df, data_str], axis=1)
    result = pd.DataFrame()
    for i in l:
        if (i in str_list):
            result = pd.concat([result, data_str[i]], axis=1)
        else:
            result = pd.concat([result, normal_df[i]], axis=1)
    if (label != None):
        data_copy[label] = result
        return data_copy
    return result


