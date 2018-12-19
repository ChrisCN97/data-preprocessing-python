
def cut(data, piece_sz=5):
    '''
    将DataFrame切片，转换成JSON格式数据，并用迭代器返回
    piece_sz: 切片大小，单位 - 行数，默认一个切片5行数据
    '''
    i = 0
    size = data.size
    while i < size:
        yield data[i:i + piece_sz]
        i += piece_sz

if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv('test/test-data/bank.csv', ';')
    i = 0
    for piece in cut(df):
        print(piece)
        print()
        i += 1
        if i > 3:
            break