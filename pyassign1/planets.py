"""solar_system.py: emulate the revolution of the Mercury, Venus,
Earth, Mars, Jupiter and Saturn around the sun.

__author__ = "Xiang Liyuan"
__pkuid__  = "1800011800"
__email__  = "xiangliyuan@pku.edu.cn"
"""
from turtle import *
from math import sin, cos, pi


# 画布参数
bg = Screen()
bg.bgcolor('#00035b')  # dark blue


# 行星参数
planet = []
color = ['#89a0b0', '#fcc006', '#247afd',
         '#fe4b03','#ffd8b1', '#d3b683']
# blueish grey, marigold, clear blue
# blood orange, light peach, very light brown
r = [0.2, 0.4, 0.4, 0.3, 1.2, 1.2]
initial_a = [0.44, 0.8, 1.0, 1.424, 1.9, 2.7]
e = [0.2056, 0.0068, 0.0167, 0.0934, 0.0483, 0.0560]
a = []
b = []
initial_step = [1.5, 3, 4, 8, 14, 20]
step = []
tracer(False)
for n in range(0, 6, 1):
    planet.append(n)
    planet[n] = Turtle()
    planet[n].color(color[n])
    planet[n].shape("circle")
    planet[n].shapesize(r[n], r[n], 1)
    a.append(initial_a[n] * 100)
    b.append(a[n] * (1 - e[n]) ** (1/2))
    step.append(initial_step[n] * 90)


# 太阳参数
sun = Turtle()
sun.color('#ffdf22')  # sun yellow
sun.shape("circle")
sun.shapesize(2.0, 2.0, 1)


# 行星初始状态
def init():
    for n in range(0, 6, 1):
        planet[n].hideturtle()
        planet[n].up()
        planet[n].setx(a[n] - a[n]*e[n])
        planet[n].sety(0)
        planet[n].down()
        planet[n].showturtle()


# 行星运动
def move():
    j = 0
    while True:
        j = j+1
        for i in range(0, 6, 1):
            if TurtleScreen._RUNNING is True:
                planet[i].goto(a[i] * cos(2 * pi * j / step[i]) - a[i] * e[i], b[i] * sin(2 * pi * j / step[i]))
            else:
                return


# 主模块
def main():
    init()
    tracer(True)
    move()


if __name__ == "__main__":
    main()
