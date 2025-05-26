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
'''

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

"""
# 模块调用测试

# 这是 import 函数名 方式调用的测试代码
import  ComputeModule
ComputeModule.G_a = 100 # 修改ComputeModule模块中的全局变量G_a的值
ComputeModule.G_b = 100 # 修改ComputeModule模块中的全局变量G_b的值
ComputeModule.print_G()
print(ComputeModule.add(1,2))
print(ComputeModule.mul(5,5))

# 这是 from 模块名 import 函数名 方式调用的测试代码
from ComputeModule import print_G,add,mul,G_a,G_b
G_a = 100  # 这个赋值操作,让main.py模块中的G_a变量指向一个新的对象,而不是修改ComputeModule命名空间中的G_a变量,这个G_a变量与ComputeModule命名空间中的G_a变量是两个不同的对象
G_b = 100  # 这个赋值操作,让main.py模块中的G_b变量指向一个新的对象,而不是修改ComputeModule命名空间中的G_b变量,这个G_b变量与ComputeModule命名空间中的G_b变量是两个不同的对象

# 因此,对于不可变对象类型变量,没有必要使用from模块名 import 函数名 方式调用,因为这种方式会创建一个新的变量,与直接创建一个变量并赋值的效果相同,除非你需要在main.py模块中使用ComputeModule命名空间中的变量值(例如你想知道当前ComputeModule中的G_a和G_b的值),否则不需要使用这种方式调用。

print_G()
print(add(1,2))
print(mul(5,5))

# 以上这两种方法:当对变量进行赋值操作时,main.py模块会在自己的命名空间中创建一个新的变量,而不是修改ComputeModule命名空间中的变量;当对可变类型变量进行修改操作时(例如:用append()方法增加元素),会直接修改ComputeModule命名空间中的变量,因为可变类型变量的引用指向的是同一个对象。需要注意的是,不可变类型变量只能进行赋值操作,不能直接修改内容。
"""