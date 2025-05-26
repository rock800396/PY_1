print("载入计算模块")
# 定义全局变量并赋给初始值
G_a = 10
G_b = 10
# 加法计算模块
def add(a,b):
    return a+b
# 乘法计算模块
def mul(a,b):
    return a*b
# 输出G_a和G_b的值
def print_G():
    print("G_a的值为：",G_a)
    print("G_b的值为：",G_b)