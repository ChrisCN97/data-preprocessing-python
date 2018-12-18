import pandas as pd
import numpy as np

'''
接口2.2 noise_process
# 数据噪声处理（平均值去噪、边界值去噪、中值去噪）
# made by 张晋豪, 2018.12.18
'''


# 去噪处理函数（noise_process），method参数不同取值
# 0：平均值
# 1：边界值
# 2：中值
def noise_process(data, method):
    row = data.shape[0]  # 行
    col = data.shape[1]  # 列
    list = data.columns.values.tolist()  # 属性列表
    array = np.array(data.values)  # numpy数组

    if method == 0:  # 0：平均值
        array_copy = array.copy()
        array_rank = np.array(np.zeros(row * col)).reshape(row, col)
        array2rank = np.array(np.zeros(row * col)).reshape(row, col)
        for i in range(col):
            array_rank[:] = array_copy.argsort(0)  # 排序后的数组该位置对应原始数组的位置
            array.sort(0)

        # array已排序
        # array_copy为原始数组
        # array_rank排序后到排序前
        # array2rank排序前到排序后

        for i in range(row):
            for j in range(col):
                array2rank[int(array_rank[i, j]), j] = i

        # array[i, j] == array_copy[int(array_rank[i, j]), j] 为真
        # array_copy[i, j] ==  array[int(array2rank[i, j]), j] 为真

        count = 0
        k = 0
        for i in range(row):
            start = int(k / 10.0 * row)
            end = int((k + 1) / 10.0 * row)
            List = array_rank[start:end].astype(int)
            for j in range(col):
                mean = np.sum(array_copy[List, j]) / (1 / 10.0 * row)
                # array[array2rank[start,i], i] = mean
                array_copy[int(array_rank[i, j]), j] = mean
            count += 1
            if (count % (row / 10) == 0):
                k += 1

    # up = array_copy2[end, j]
    elif method == 1:  # 1：边界值
        array_copy = array.copy()
        array_copy2 = array.copy()
        array_rank = np.array(np.zeros(row * col)).reshape(row, col)
        array2rank = np.array(np.zeros(row * col)).reshape(row, col)
        for i in range(col):
            array_rank[:] = array_copy.argsort(0)  # 排序后的数组该位置对应原始数组的位置
            array.sort(0)

        # array已排序
        # array_copy为原始数组
        # array_rank排序后到排序前
        # array2rank排序前到排序后

        for i in range(row):
            for j in range(col):
                array2rank[int(array_rank[i, j]), j] = i

        # array[i, j] == array_copy[int(array_rank[i, j]), j] 为真
        # array_copy[i, j] ==  array[int(array2rank[i, j]), j] 为真

        count = 0
        k = 0
        for i in range(row):
            start = int(k / 10.0 * row)
            end = int((k + 1) / 10.0 * row) - 1
            for j in range(col):
                up = array_copy2[end, j]
                array_copy[int(array_rank[i, j]), j] = up
            count += 1
            if (count % (row / 10) == 0):
                k += 1

    elif method == 2:  # 2：中值
        array_copy = array.copy()
        array_copy2 = array.copy()
        array_rank = np.array(np.zeros(row * col)).reshape(row, col)
        array2rank = np.array(np.zeros(row * col)).reshape(row, col)
        for i in range(col):
            array_rank[:] = array_copy.argsort(0)  # 排序后的数组该位置对应原始数组的位置
            array.sort(0)

        # array已排序
        # array_copy为原始数组
        # array_rank排序后到排序前
        # array2rank排序前到排序后

        for i in range(row):
            for j in range(col):
                array2rank[int(array_rank[i, j]), j] = i

        # array[i, j] == array_copy[int(array_rank[i, j]), j] 为真
        # array_copy[i, j] ==  array[int(array2rank[i, j]), j] 为真

        count = 0
        k = 0
        for i in range(row):
            start = int(k / 10.0 * row)
            end = int((k + 1) / 10.0 * row) - 1
            for j in range(col):
                Middle = array_copy2[int((start + end) / 2), j]
                array_copy[int(array_rank[i, j]), j] = Middle
            count += 1
            if (count % (row / 10) == 0):
                k += 1

    normal_df = pd.DataFrame(array_copy, index=range(row), columns=list)
    return normal_df