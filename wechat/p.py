import itchat
from pyecharts import options as opts
from pyecharts.charts import Pie
# 导入jieba模块，用于中文分词
import jieba
# 导入matplotlib，用于生成2D图形
import matplotlib.pyplot as plt
# 导入wordcount，用于制作词云图
from wordcloud import WordCloud, STOPWORDS




# 获取数据
def get_data():
    # 扫描二维码登陆微信，实际上就是通过网页版微信登陆
    itchat.auto_login(hotReload=True)

    # 获取所有好友信息
    friends = itchat.get_friends(update=True)  # 返回一个包含用户信息字典的列表
    return friends


# 处理数据
def parse_data(data):
    friends = []
    for item in data[1:]:  # 第一个元素是自己，排除掉
        friend = {
            'NickName': item['NickName'],  # 昵称
            'RemarkName': item['RemarkName'],  # 备注名
            'Sex': item['Sex'],  # 性别：1男，2女，0未设置
            'Province': item['Province'],  # 省份
            'City': item['City'],  # 城市
            'Signature': item['Signature'].replace('\n', ' ').replace(',', ' '),  # 个性签名（处理签名内容换行的情况）
            'StarFriend': item['StarFriend'],  # 星标好友：1是，0否
            'ContactFlag': item['ContactFlag']  # 好友类型及权限：1和3好友，259和33027不让他看我的朋友圈，65539不看他的朋友圈，65795两项设置全禁止
        }
        print(friend)
        friends.append(friend)
    return friends


if __name__ == '__main__':
    pass
    # print(parse_data(get_data()))


# 存储数据，存储到文本文件
def save_to_txt():
    friends = parse_data(get_data())
    with open('friends.txt', mode='w', encoding='utf-8') as f:
         for item in friends:
                f.write('%s,%s,%d,%s,%s,%s,%d,%d\n' % (
                item['NickName'], item['RemarkName'], item['Sex'], item['Province'], item['City'], item['Signature'],
                item['StarFriend'], item['ContactFlag']))


if __name__ == '__main__':
    save_to_txt()



def getSex():
    # 获取所有性别
    sex = []
    with open('friends.txt', mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            sex.append(row.split(',')[2])
    # print(sex)
    print(len(sex));

    # 统计每个性别的数量
    attr = ['帅哥', '美女', '未知']
    value = [sex.count('1'), sex.count('2'), sex.count('0')]
    print(value)
    pie = (
        Pie()
            .add("", [list(z) for z in zip(attr, value)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    pie.render('好友性别比例.html')

getSex();


# 获取所有个性签名
signatures = []
with open('friends.txt', mode='r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        signature = row.split(',')[5]
        if signature != '':
            signatures.append(signature)
            signature.replace('\u3000', ' ')

# 设置分词
split = jieba.cut(str(signatures), cut_all=False)  # False精准模式分词、True全模式分词
words = ' '.join(split)  # 以空格进行拼接
# print(words)

# 设置屏蔽词，去除个性签名中的表情、特殊符号等
stopwords = STOPWORDS.copy()
stopwords.add('span')
stopwords.add('class')
stopwords.add('emoji')
stopwords.add('emoji1f334')
stopwords.add('emoji1f388')
stopwords.add('emoji1f33a')
stopwords.add('emoji1f33c')
stopwords.add('emoji1f633')

# 导入背景图
bg_image = plt.imread('bg.jpg')

# 设置词云参数，参数分别表示：画布宽高、背景颜色、背景图形状、字体、屏蔽词、最大词的字体大小
wc = WordCloud(width=1024, height=768, background_color='white', mask=bg_image, font_path='STKAITI.TTF',
               stopwords=stopwords, max_font_size=400, random_state=50)
# 将分词后数据传入云图
wc.generate_from_text(words)
plt.imshow(wc)  # 绘制图像
plt.axis('off')  # 不显示坐标轴
# 保存结果到本地
wc.to_file('个性签名词云图.jpg')



