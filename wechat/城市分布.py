from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def render():
    # 获取所有城市
    cities = []
    with open('friends.txt', mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            city = row.split(',')[4]
            if city != '':  # 去掉城市名为空的值
                cities.append(city)
    # 统计每个城市出现的次数
    data = Counter(cities).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表
    print(data)

    fri_cities = [];
    fri_num = [];
    for k in range(len(list(data))):
       fri_cities.append(data[k][0])
       fri_num.append(data[k][1])
    print(fri_cities)
    print(fri_num)

    matplotlib.rcParams['font.family'] = 'SimHei'
    N = len(list(data))
    x = np.arange(N)
    # 绘图 x x轴， height 高度, 默认：color="blue", width=0.8
    p1 = plt.bar(x, height=fri_num, width=0.5, label="城市指标", tick_label=fri_cities)

    # 添加数据标签
    for a, b in zip(x, fri_num):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)

    # 添加图例
    #plt.legend()

    # 展示图形
    plt.show()

render()
