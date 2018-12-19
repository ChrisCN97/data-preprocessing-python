'''
# 接口 4.1、4.2、4.3
# author: 蒲治北
'''

import numpy as np
import operator
import math
import matplotlib.pyplot as plt


# loadDataSet(fileName, n)函数加载数据，n代表是用户指定的第n列数据
# draw_bar用于绘制条形图，drawPie绘制饼图，drawLine绘制折线图
# is_number用于判断用户该列数据是否是数字，若是，draw_bar函数调用def drawHist绘制直方图，否则调用drawBar绘制条形图
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def loadDataSet(fileName, n):
    data = []
    fr = open(fileName)
    # 第一行是每一列数据的名称，绘图时不需要第一行
    first_line = fr.readline()
    label_line = first_line.strip().split(';')
    labels = list(label_line)
    # 去掉split时默认加上的引号
    label = eval(labels[n - 1])
    for line in fr.readlines():
        curLine = line.strip().split(';')
        fltLine = list(curLine)
        data.append(eval(fltLine[n-1]))
    return label, data

def drawHist(label, data):
    ax1 = plt.subplot(111)
    data1 = np.array(data)
    ax1.hist(data1, bins=int((max(data)-min(data))/10), density=0, histtype='stepfilled')
    # 横轴每一个柱体名称太长会导致显示重叠，对字体进行旋转以消除重叠
    plt.xticks(rotation=300)
    # 横纵轴名称
    plt.xlabel(label)
    plt.ylabel('Frequency')
    return plt


def drawBar(label, data):
    ax1 = plt.subplot(111)
    xticks = {}
    for attrValue in data:
        xticks[attrValue] = xticks.get(attrValue, 0) + 1
    rects = ax1.bar(range(len(xticks)), [xticks.get(xtick, 0) for xtick in list(xticks.keys())], align='center')
    # 横轴每一个柱体名称太长会导致显示重叠，对字体进行旋转以消除重叠
    plt.xticks(rotation=300)
    # 给每一个柱体命名
    plt.xticks(range(len(xticks)), list(xticks.keys()))
    plt.xlabel(label)
    plt.ylabel('Frequency')
    # 标注柱体的数值
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom')
    return plt

def draw_bar(label, data):
    if is_number(data[0]):
        return drawHist(label, data)
    else:
        return drawBar(label, data)


def draw_pie(label, data):
    ax1 = plt.subplot(111)
    xticks = {}
    labels = []
    sizes = []
    # 如果数据是数字，应该将数据分区间统计然后绘制饼图，否则直接统计每一种数据的数量绘制饼图
    if is_number(data[0]):
        values = []
        dist = (max(data) - min(data)) / 5
        for i in range(6):
            values.append(min(data)+dist*i)
        for i in range(2):
            labels.append(str(int(values[i])) + '-' + str(int(values[i + 1])))
            # 由于数据一般服从正态分布，导致首尾的区间包含个数少，导致饼图中这些区间面积小，文字显示重叠，所以这里没有将区间按大小顺序排序
        labels.append(str(int(values[4])) + '-' + str(int(values[5])))
        labels.append(str(int(values[2])) + '-' + str(int(values[3])))
        labels.append(str(int(values[3])) + '-' + str(int(values[4])))
        # 统计数据
        for attrValue in data:
            if min(data) < attrValue < min(data) + dist:
                xticks[values[0]] = xticks.get(values[0], 0) + 1
            elif min(data) + dist <= attrValue < min(data) + 2*dist:
                xticks[values[1]] = xticks.get(values[1], 0) + 1
            elif min(data) + 2*dist <= attrValue < min(data) + 3*dist:
                xticks[values[2]] = xticks.get(values[2], 0) + 1
            elif min(data) + 3*dist <= attrValue < min(data) + 4*dist:
                xticks[values[3]] = xticks.get(values[3], 0) + 1
            else:
                xticks[values[4]] = xticks.get(values[4], 0) + 1
        # 统计频率
        count = len(data)
        key = list(xticks.keys())
        # 和前面的标签顺序保持一致
        for i in range(2):
            sizes.append(xticks[key[i]]/count)
        sizes.append(xticks[key[4]] / count)
        sizes.append(xticks[key[2]] / count)
        sizes.append(xticks[key[3]] / count)
    # 若数据不是数值类型，不用分区，直接统计
    else:
        for attrValue in data:
            xticks[attrValue] = xticks.get(attrValue, 0) + 1
        count = len(data)
        for value in xticks.values():
            sizes.append(value/count)
        labels = list(xticks.keys())
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=False, labeldistance=1.1, startangle=90)
    plt.xlabel(label)
    return plt


def draw_line(label, data):
    ax1 = plt.subplot(111)
    data.sort()
    x = range(len(data))
    ax1.plot(x, data)
    return plt
