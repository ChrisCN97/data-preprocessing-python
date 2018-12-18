
import pandas as pd
from module.packed import *

def test_normalize():
    file = pd.read_table('test-data/bank.csv', ';')
    trainData = file.iloc[0:4000][
        ['balance', 'age', 'day', 'duration', 'campaign', 'previous', 'pdays']].astype('float')
    print(normalize(trainData, 2))

def test_noise_process():
    file = pd.read_table('test-data/bank.csv', ';')
    trainData = file.iloc[0:4000][
        ['balance', 'age', 'day', 'duration', 'campaign', 'previous', 'pdays']].astype('float')
    df = noise_process(trainData, 2)
    print(df)

def test_null_process():
    data = read_file('test-data/back.csv')
    method = 2
    data = null_process(data, method)
    print(data)

def loadDataSet(fileName, n):
    data = []
    fr = open(fileName)
    first_line = fr.readline()
    label_line = first_line.strip().split(';')
    labels = list(label_line)
    label = eval(labels[n - 1])
    for line in fr.readlines():
        curLine = line.strip().split(';')
        fltLine = list(curLine)
        data.append(eval(fltLine[n-1]))
    return label, data

def test_visualization():
    filename = 'test-data/bank.csv'
    label, data = loadDataSet(filename, 1)
    draw_line(label, data)

