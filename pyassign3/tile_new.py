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
            h = [i * length, j * length, 1]
            list1.append(0)
            list1[-1] = copy.deepcopy(h)
    return list1


# 对于长方形的砖

# 以墙的左上角为起点，尝试在坐标为（x，y）处向右下方铺砖
# 铺砖信息记录在列表bricks中


def lay_try(x, y, kind):
    if kind == 1:   # 砖竖放
        ax = width
        by = length
    if kind == 2:   # 砖横放
        ax = length
        by = width
        
    if (x + ax - 1) > (m - 1) or (y + by - 1) > (n - 1):  # 越界则返回错误
        return False
    for c1 in range(x, x + ax):  # 无法铺则返回错误
        for c2 in range(y, y + by):
            if wall[c2][c1] == 1:
                return False
    for c1 in range(x, x + ax):  # 铺砖
        for c2 in range(y, y + by):
            wall[c2][c1] = 1
    info = (x, y, kind)  # 记录铺的砖的位置，放置状态
    for i in range(x, x + ax):  # 修改记录每列最靠上的未铺砖格子的列表
        position[i] = y + by
    bricks.append(info)
    return info



# 撤销左上角的格子的坐标为（x， y）的一块砖
def del_lay(x, y, i):
    if i == 1:   # 原来竖放
        ax = width
        by = length
    if i ==2:    # 原来横放
        ax = length
        by = width

    for c1 in range(x, x + ax):
        for c2 in range(y, y + by):
            wall[c2][c1] = 0
    posi_1 = bricks[-1]
    del bricks[-1]
    for i in range(x, x + ax):
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


# 尝试铺砖
def lay_brick(x, y, i):
    
    if i == 1:  # 竖放
        brick = lay_try(x, y, 1)  # 竖着铺一块砖
        if brick != 0:
            posi_1 = search()  # 符合条件的未铺砖的格子
            if posi_1[1] == n:   # 判断一种方法是否铺完
                # print("Find a method 1",posi_1)
                return
            lay_brick(posi_1[0], posi_1[1], 1)
        else:  # 若不能，则竖铺
            lay_brick(x, y, 2)


    if i == 2:
        brick = lay_try(x, y, 2)  # 横着铺一块砖
        if brick != 0:
            posi_1 = search()
            if posi_1[1] == n:   # 判断一种方法是否铺完
                # print("Find a method 2",posi_1)
                return
            lay_brick(posi_1[0], posi_1[1], 1)
        else:  # 若不能，则去砖
            lay_brick(x, y, 3)

    if i == 3:
        if x == 0 and y == 0:
            # curpos = [x, y, i] #??????????????????????????????????
            print("Pass 0")
            return  # 全部解已经找到，结束搜索
        else:
            if len(bricks) > 0:  # 判断是否把砖去到第一块
                # print("Pass 3", x, y, i, bricks[-1][0], bricks[-1][1], bricks[-1][2])
                posi_1 = del_lay(bricks[-1][0], bricks[-1][1], bricks[-1][2])
                # print("Pass 3-1", x, y, i, posi_1)
                lay_brick(posi_1[0], posi_1[1], posi_1[2] + 1)
            elif len(bricks) == 0:
                # curpos = [x, y, i]  #??????????????????????????????????
                print("Pass 1")
                return  # 全部解已经找到，结束搜索



# 将格式转换为标准输出格式
def trans(x, y, i):
    list_1 = []
    if i == 1:
        for add1 in range(length):
            for add2 in range(width):
                list_1.append((x + add2) + (y + add1) * m)
    elif i == 2:
        for add1 in range(width):
            for add2 in range(length):
                list_1.append((x + add2) + (y + add1) * m)
    return list_1


def main():
    word = '所选规格的砖不能铺满整面墙'
    side = input_tile()
    ju = judge(side[0], side[1])
    
    if ju is True:
        is_sq = is_squ()
        if is_sq is True:
            list1 = squ()
            for i in range(int((m * n) / (length * width))):
                list1[i] = copy.deepcopy(trans(list1[i][0], list1[i][1], list1[i][2]))
            print(list1)
        else:
            global position, bricks, result, method, curpos
            position = [0] * m  # 记录每列未铺砖的列序号最小的格子
            bricks = []  # 记录已铺的所有砖的信息
            result = []  # 记录结果
            curpos = [0] * m  #??????????????????????????????????
            form()

            x = y = 0
            i = 1
            # ways = 0

            time_start = time.process_time()
            while  x != 0 or y !=0 or i != 3:
                # way1 = ways // 1000000
                lay_brick(x, y, i)
                # print(curpos)   #??????????????????????????????????
                if len(bricks) == 0:
                    break
                # ways = ways +1
                # way2 = ways // 1000000
                # if way1  != way2:
                #    print(way2, 'million ways')
                result.append(0)
                result[-1] = copy.deepcopy(bricks)
                x = m  #以下三行是在旧方法基础上，去掉倒数第一砖，重铺寻找新解
                y = n
                i = 3


            #print(ways, ' ways in total')
            method = len(result)
            print('method=', method)
            elapsed = (time.process_time() - time_start)
            print("Time used:",elapsed)

            if method == 0:
               print(word)
            # else:
            #    for i in range(method):
            #        for j in range(int((m * n) / (length * width))):
            #            result[i][j] = copy.deepcopy(trans(result[i][j][0], result[i][j][1], result[i][j][2]))
                # for i in result:
                #    print(tuple(i))
    elif ju == 0:
        print(word)

# 选择一种实现图像表示


if __name__ == '__main__':
    main()
