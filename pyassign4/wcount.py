"""wcount.py: count words from an Internet file.

__author__ = "Xiang Liyuan"
__pkuid__  = "1800011800"
__email__  = "xiangliyuan@pku.edu.cn"
"""

import sys
from string import punctuation
from urllib.request import urlopen
import urllib.error


def wcount(lines, topn=10):
    """count words from lines of text string, then sort by their counts
    in reverse order, output the topn (word count), each in one line.
    """

    after_lines = lines.split()  # 用空格分割字符串
    lines = []
    for i in after_lines:
        i = i.split('--')
        for j in i:  # 用破折号再次分割字符串
            lines.append(j)
    count = {}
    for i in range(len(lines)):  # 处理数据， 去标点符号并把所有单词转为小写
        lines[i] = lines[i].strip(punctuation)
        lines[i] = lines[i].lower()
        for k in list(lines[i]):  # 去除都是数字的字符
            if k.isnumeric() == 1:
                break
        else:  # 单词计数,不计入页面上网址
            if lines[i] not in count and ''.join(list(lines[i])[:4]) != 'http' \
                    and ''.join(list(lines[i])[-4:]) != '.org' and lines[i] != '':
                count[lines[i]] = 1
            elif lines[i] in count:
                count[lines[i]] += 1
    word_count = list(map(lambda x, y: (x, y), count.keys(), count.values()))  # 字典转列表
    word_count.sort(key=lambda d: d[1], reverse=True)  # 排序
    if topn > len(word_count):
        topn = len(word_count)
    for i in range(topn):  # 输出答案
        print(word_count[i][0], word_count[i][1])
    pass


if __name__ == '__main__':

    if len(sys.argv) == 1:  # 若用户未给出任何参数
        print('Usage: {} url [topn]'.format(sys.argv[0]))
        print('  url: URL of the txt file to analyze ')
        print('  topn: how many (words count) to output. If not given, will output top 10 words')
        sys.exit(1)
    elif len(sys.argv) == 2 or len(sys.argv) == 3:  # 若用户给出的参数个数符合要求
        url = sys.argv[1]
        try:
            doc = urlopen(url)
            docstr = doc.read()
            doc.close()
        except urllib.error.HTTPError as e:  # 处理异常
            print('Error:', e.code, e.reason)
        except urllib.error.URLError as e:
            print(e.reason)
        else:  # 将网页转换为字符串
            docstr = docstr.decode()
            if len(sys.argv) == 3:
                topn = int(sys.argv[2])
            else:
                topn = 10
            wcount(docstr, topn)
    elif len(sys.argv) > 3:  # 若用户给出多于2个参数
        print('Error: The number of data you input is more than 2.')
