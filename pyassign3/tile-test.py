import copy
import sys
import time
sys.setrecursionlimit(100000000)


def input_tile():
    global m, n, length, width
    print('请输入墙与瓷砖的长宽' +
          '\n墙的长度: ')
    m = int(input())
    print('墙的宽度： ')
    n = int(input())
    print('砖的长度： ')
    length = int(input())
    print('砖的宽度： ')
    width = int(input())
    a = max(length, width)
    b = min(length, width)
    return a, b


def calcu(long, a, b):  # 墙的两边长能否被均能表示为若干块砖的长、宽之和
    e = long // a
    f = 0
    while long != e * a + b * f and e >= 0 and f >= 0:
        e = e - 1
        f = (long - e * a) // b
    if long == e * a + b * f:
        return True
    else:
        return False


def judge(a, b):  # 初步判断铺满砖的可行性
    if (m * n) % (length * width) != 0:
        return 0
    else:
        t = calcu(n, a, b)
        s = calcu(m, a, b)
        if t is True and s is True:
            return True
        else:
            return False


def form():  # 建立描述墙的初始状态的二维数组,数组有n项，与竖直方向对应；每项中有m项，与水平方向对应
    global wall
    wall = [([0] * m) for i in range(n)]


# 对于正方形的砖
def is_squ():  # 判断是否为正方形
    if length == width:
        return True
    else:
        return False


# 判断正方形砖可不可铺满。如可铺满，返回每块砖左上角格子的坐标。
def squ():
    list1 = []
    for i in range(0, m//length):
        for j in range(0, n//length):
            h = [j * length, i * length, 1]
            list1.append(0)
            list1[-1] = copy.deepcopy(h)
    return list1


# 对于长方形的砖

# 以墙的左上角为起点，尝试在坐标为（x，y）处向右下方铺砖
# 铺砖信息记录在列表bricks中


def lay_type(x, y, i):  # 铺一块砖
    if i == 1:  # 横着铺砖
        side_x = length
        side_y = width
    elif i == 2:  # 竖着铺砖
        side_x = width
        side_y = length
    if (x + side_x - 1) > (m - 1) or (y + side_y - 1) > (n - 1):  # 越界则返回错误
        return False
    for c1 in range(x, x + side_x):  # 无法铺则返回错误
        for c2 in range(y, y + side_y):
            if wall[c2][c1] == 1:
                return False
    for c1 in range(x, x + side_x):  # 铺砖
        for c2 in range(y, y + side_y):
            wall[c2][c1] = 1
    info = (x, y, i)  # 记录铺的砖的位置，放置状态
    for i in range(x, x + side_x):  # 修改记录每行未铺砖格子的列表
        position[i] = y + side_y
    bricks.append(info)
    return info


# 撤销左上角的格子的坐标为（x， y）的一块砖
def del_lay(x, y, i):
    if i == 1:  # 横放
        side_x = length
        side_y = width
    elif i == 2:  # 竖放
        side_x = width
        side_y = length
    for c1 in range(x, x + side_x):
        for c2 in range(y, y + side_y):
            wall[c2][c1] = 0
    posi_1 = bricks[-1]
    del bricks[-1]
    for i in range(x, x + side_x):
        position[i] = y
    return posi_1  # 返回撤销的砖的位置及放置参数


# 寻找要铺的砖
def search():
    y = min(position)
    if y <= n - 1:
        x = position.index(y)
    elif y == n:
        x = m
    return [x, y]


# 尝试铺砖，找出第一种铺砖方法
def lay_brick(x=0, y=0, i=1):
    if i == 1:  # 横放
        brick = lay_type(x, y, 1)  # 横着铺一块砖
        if brick != 0:
            posi_1 = search()  # 符合条件的未铺砖的格子
            if posi_1[1] == n:   # 判断一种方法是否铺完
                return
            lay_brick(posi_1[0], posi_1[1], 1)
        else:  # 若不能横铺
            lay_brick(x, y, 2)

    elif i == 2:
        brick = lay_type(x, y, 2)  # 竖着铺一块砖
        if brick != 0:
            posi_1 = search()
            if posi_1[1] == n:   # 判断一种方法是否铺完
                return
            lay_brick(posi_1[0], posi_1[1], 1)
        else:
            lay_brick(x, y, 3)

    elif i == 3:
        if x == 0 and y == 0:
            return
        else:
            posi_1 = del_lay(bricks[-1][0], bricks[-1][1], bricks[-1][2])
            lay_brick(posi_1[0], posi_1[1], posi_1[2] + 1)


# 将格式转换为标准输出格式
def trans(x, y, i):
    list_1 = []
    if i == 1:  # 横放
        side_x = length
        side_y = width
    elif i == 2:  # 竖放
        side_x = width
        side_y = length
    for add1 in range(side_y):
        for add2 in range(side_x):
            list_1.append(str((x + add2) + (y + add1) * m))
    str_tuple = '(' + (', '.join(list_1)) + ')'
    return str_tuple


def main():
    word = '所选规格的砖不能铺满整面墙'
    side = input_tile()
    time_start = time.process_time()
    ju = judge(side[0], side[1])
    if ju is True:
        is_sq = is_squ()

        if is_sq is True:
            list_1 = squ()
            print('铺砖方法共：' + str(1) + '种')
            for i in range(int((m * n) / (length * width))):
                list_1[i] = copy.deepcopy(trans(list_1[i][0], list_1[i][1], list_1[i][2]))
            print('[' + ', '. join(list_1) + ']')

        else:
            global position, bricks, result, method
            position = [0] * m  # 记录每列未铺砖的列序号最小的格子
            bricks = []  # 记录已铺的所有砖的信息
            result = []  # 记录结果

            form()

            x = y = 0
            i = 1
            while x != 0 or y != 0 or i != 3:
                lay_brick(x, y, i)
                if len(bricks) == 0:
                    break
                result.append(0)
                result[-1] = copy.deepcopy(bricks)
                x = m  # 以下三行是去掉倒数第一砖，重铺寻找新解
                y = n
                i = 3

            method = len(result)
            if method == 0:
                print(word)
            else:
                print('铺砖方法共：' + str(method) + '种')
                for i in result:
                    print(i)
                elapsed = (time.process_time() - time_start)
                print("Time used:",elapsed)
                for i in range(method):
                    for j in range(int((m * n) / (length * width))):
                        result[i][j] = copy.deepcopy(trans(result[i][j][0], result[i][j][1], result[i][j][2]))
                    # print('[' + ', '. join(result[i]) + ']')
        elapsed = (time.process_time() - time_start)
        print("Time used:", elapsed)
    elif ju == 0:
        print(word)

# 选择一种实现图像表示


if __name__ == '__main__':
    main()
