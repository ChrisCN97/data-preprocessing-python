import pandas as pd

'''
# 接口2.3 normalize
# 数据预处理函数（normalize），小数定标法辅助函数（find_tens）
# made by 张晋豪, 2018.12.18
'''


# method参数不同取值
# 0 min-max
# 1 z-score
# 2 小数定标
def normalize(data, method):
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
    data_number = data[number_list]

    row = data_number.shape[0]  # 行
    col = data_number.shape[1]  # 列
    list = data_number.columns.values.tolist()  # 属性列表
    array = data_number.astype(float).values  # numpy数组

    if method == 0:  # min-max
        for i in range(col):
            min = array[:, i].min()
            max = array[:, i].max()
            array[:, i] = (array[:, i] - min) / (max - min)

    elif method == 1:  # z-score
        for i in range(col):
            mean = array[:, i].mean()
            std = array[:, i].std()  # 标准差
            array[:, i] = (array[:, i] - mean) / std

    elif method == 2:  # 小数定标
        for i in range(col):
            max = array[:, i].max()
            tens = find_tens(max)
            ten_up = 10 ** tens
            array[:, i] = array[:, i] / ten_up

    normal_df = pd.DataFrame(array, index=range(row), columns=list)
    # normal_df = pd.concat([normal_df, data_str], axis=1)
    result = pd.DataFrame()
    for i in l:
        if (i in str_list):
            result = pd.concat([result, data_str[i]], axis=1)
        else:
            result = pd.concat([result, normal_df[i]], axis=1)
    return result


# 需要一个10的x次方，使其刚好大于Number值，返回x
def find_tens(Number):
    number = abs(Number)
    for i in range(-10, 11):
        if (number / (10 ** i) < 1):
            return i
