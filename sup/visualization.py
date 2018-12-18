'''
# 接口 4.1、4.2、4.3
# author: 蒲治北
'''

import numpy as np
import operator
import math
import matplotlib.pyplot as plt


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


def drawHist(label, data):
    ax1 = plt.subplot(111)
    data1 = np.array(data)
    ax1.hist(data1, bins=int((max(data)-min(data))/10), density=0, histtype='stepfilled')
    plt.xticks(rotation=300)
    plt.xlabel(label)
    plt.ylabel('Frequency')
    return plt


def drawBar(label, data):
    ax1 = plt.subplot(111)
    xticks = {}
    for attrValue in data:
        xticks[attrValue] = xticks.get(attrValue, 0) + 1
    rects = ax1.bar(range(len(xticks)), [xticks.get(xtick, 0) for xtick in list(xticks.keys())], align='center')
    plt.xticks(rotation=300)
    plt.xticks(range(len(xticks)), list(xticks.keys()))
    plt.xlabel(label)
    plt.ylabel('Frequency')
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
    if is_number(data[0]):
        values = []
        dist = (max(data) - min(data)) / 5
        for i in range(6):
            values.append(min(data)+dist*i)
        for i in range(2):
            labels.append(str(int(values[i])) + '-' + str(int(values[i + 1])))
        labels.append(str(int(values[4])) + '-' + str(int(values[5])))
        labels.append(str(int(values[2])) + '-' + str(int(values[3])))
        labels.append(str(int(values[3])) + '-' + str(int(values[4])))
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
        count = len(data)
        key = list(xticks.keys())
        for i in range(2):
            sizes.append(xticks[key[i]]/count)
        sizes.append(xticks[key[4]] / count)
        sizes.append(xticks[key[2]] / count)
        sizes.append(xticks[key[3]] / count)
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
