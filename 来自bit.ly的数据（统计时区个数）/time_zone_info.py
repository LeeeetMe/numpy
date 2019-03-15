from collections import defaultdict
from collections import Counter
import json
from pandas import DataFrame, Series
import numpy as np
import pandas as pd

path = 'example.txt'


def get_file_list(path):
    file_list = list()
    with open(path, 'r') as file:
        for line in file:
            line = json.loads(line)
            if 'tz' in line:
                file_list.append(line.get('tz'))

    return file_list


def get_tz_counter(li):
    counters = defaultdict(int)
    for l in li:
        print(type(l), l)
        if l in counters:
            counters[l] += 1
        else:
            counters[l] = 1
    return counters


def get_top_tz(tz_dict, n):
    tz_list = list()
    for key, val in tz_dict.items():
        tz_list.append((val, key))
    tz_list.sort(reverse=True)
    return tz_list[:n]


def get_records(file_path):
    return [json.loads(line) for line in open(file_path)]


def get_top_in_python():
    file_li = get_file_list(path)
    counters = get_tz_counter(file_li)
    top_ten = get_top_tz(counters, 10)
    print(top_ten)
    print(len(top_ten))


def get_top_in_counter():
    c = Counter(get_file_list(path))
    top_ten = c.most_common(10)
    print(top_ten)
    return top_ten


if __name__ == '__main__':
    # 使用 python
    get_top_in_python()
    # 使用 Counter
    get_top_in_counter()
    # 使用numpy、pandas
    data_frame = DataFrame(get_records(path))

    clean_tz = data_frame['tz'].fillna('Missing')  # 用`Missing`替换缺失值
    clean_tz[clean_tz == ''] = 'Unknown'  # 用`Unknown`替换空白值

    tz_counts = clean_tz.value_counts()
    tz_counts[:10].plot(kind='barh', rot=0)  # 绘图，可视化的方式展示前十项
