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
    row = data.shape[0]  # 行
    col = data.shape[1]  # 列
    list = data.columns.values.tolist()  # 属性列表
    array = data.values  # numpy数组

    if method == 0:  # min-max
        for i in range(col):
            min = array[:, i].min()
            max = array[:, i].max()
            array[:, i] = (array[:, i] - min) / (max - min)

    elif method == 1:  # z-score
        for i in range(col):
            mean = array[:, i].mean()
            std = array[:, i].std()
            array[:, i] = (array[:, i] - mean) / std

    elif method == 2:  # 小数定标
        for i in range(col):
            max = array[:, i].max()
            tens = find_tens(max)
            ten_up = 10 ** tens
            array[:, i] = array[:, i] / ten_up

    normal_df = pd.DataFrame(array, index=range(row), columns=list)
    return normal_df


def find_tens(Number):
    number = abs(Number)
    for i in range(-10, 11):
        if (number / (10 ** i) < 1):
            return i

if __name__ == '__main__':
    file = pd.read_table('test-data/bank.csv', ';')
    trainData = file.iloc[0:4000][
        ['balance', 'age', 'day', 'duration', 'campaign', 'previous', 'pdays']].astype('float')
    print(normalize(trainData, 2))
