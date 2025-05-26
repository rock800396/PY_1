"""
我是多行注释
我有很多行
我主要是来测试多行注释
"""
#我再来试试单行注释
'''
我是多行注释
我有很多行
我主要是来测试多行注释
# '''
# # print("天上人间一号妹妹，你好")
# name="杨德平"
# for i in name:
#     print(i,end="")

'''
# 这是一个登陆界面中的密码输入控制代码,确保密码长度大于6位并且尝试次数不高于3次
# 当密码长度小于6位时,抛出自定义异常PwdLengthError,返回自定义错误信息
# 当尝试次数超过3次时,结束程序运行并给出提示信息
class PwdLengthError(Exception):  #声明一个继承自Exception的自定义错误PwdLengthError
    pass
Pwd_count = 0
login_result = False
def login():
    pwd = input("请输入密码:")
    if len(pwd) >= 6:
        print("密码输入成功!")
        return True
    raise  PwdLengthError("密码长度不足6位!")
while not login_result and Pwd_count < 3:
    Pwd_count += 1
    try:
        login_result = login()
    except PwdLengthError as e:
        print(f"密码长度错误:{e}")
    except Exception as e:
        print(f"发生未知错误:{e}")
        login_result = False    #冗余,用于在大型程序中检测变量状态
        break
else:
    if not login_result:
        print("密码输入错误次数过多!")
print("看到我,代表程序继续执行,只是便于观察异常处理是否成功!")
'''

# 模块调用测试
# import 函数名
# 这是 import 函数名 方式调用的测试代码
import  ComputeModule
ComputeModule.G_a = 100
ComputeModule.G_b = 100
ComputeModule.print_G()
print(ComputeModule.add(1,2))
print(ComputeModule.mul(5,5))
# 这是 from 模块名 import 函数名 方式调用的测试代码
from ComputeModule import print_G,add,mul
print_G()
print(add(1,2))
print(mul(5,5))