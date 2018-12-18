# coding=utf-8
'''
# 接口2.1 null_process
'''

import pandas as pd
import numpy as np


def _mean_process(series):
    mean = series.mean()
    return series.fillna(mean)


def _var_process(series):
    mean = series.mean()
    var = series.var()
    return series.fillna(mean - var)


def _normal_process(series):
    mean = series.mean()
    std = series.std()
    return series.apply(
        lambda x: np.random.normal(loc=mean, scale=std) if (np.isnan(x)) else x
    )


_operations = {0: _mean_process, 1: _var_process, 2: _normal_process}


def nullProcess(data, method):
    op = _operations[method]
    data = data.copy(True)
    columns = data.columns

    for col in columns:
        try:
            data[col] = op(data[col])
        except TypeError:  # 对应非数值填充
            data[col].fillna(method='ffill', inplace=True)

    return data


if __name__ == "__main__":
    data = pd.read_csv('./test.csv')
    method = 2
    data = nullProcess(data, method)
    print(data)
