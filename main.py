"""
这是天上人间一号妹妹的代码测试
"""

"""
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
"""

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

"""
# 下面进行包的测试

# # 调用方式1:这种方式导入包,可以使用包中的模块,使用函数则需要指定模块名
# import pack_01
# pack_01.login.fun_login()  # 调用登录模块中的函数
# pack_01.register.fun_register()  # 调用注册模块中的函数
# # 注意:此时需要在__init__.py文件中使用from. import login和from. import register来导入模块,可以直接使用pack_01.login.fun_login()和pack_01.register.fun_register()来调用函数

# # 调用方式2:这种方式直接导入了包中的模块,是显式调用,可以直接使用login.fun_login()和register.fun_register()来调用函数,不需要在__init__.py文件中导入模块
# from pack_01 import login, register
# login.fun_login()  # 调用登录模块中的函数
# register.fun_register()  # 调用注册模块中的函数

# # 调用方式3:
# from pack_01 import *  # 导入包中的所有模块
# login.fun_login()  # 调用登录模块中的函数
# register.fun_register()  # 调用注册模块中的函数
# # 注意:可以使用__init__.py文件中的__all__变量来控制导入的模块,如果不定义__all__变量,只会导入已经定义或导入到其自身命名空间中的名称,如果定义了__all__变量,则只会导入__all__变量中指定的模块
"""

"""
# 斐波那契数列的递归实现
# 异常处理
import sys

# 设定计数器
MaxInputCount = 3   # 最大尝试次数
AttemptCount = 0    #当前尝试次数

# 求斐波那契数列第N项目的值
def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

# 打印斐波那契数列
def print_fib(len_f=10):
    for i in range(1, len_f + 1):
        print(fib(i),end=" ")

# 接收用户输入并进行异常处理
len_f = None
while AttemptCount < MaxInputCount:
    try:
        len_f = int(input("请输入要打印的斐波那契数列长度:"))
        if len_f <= 0:                                       #如果输入值小于0,打印提示,计数器+1,程序继续执行,此时:else不会被执行;因为没有发生异常,所以异常处理代码不会被执行;会跳到while循环尾部判断输入次数是否超过最大值的if语句.如果此时尝试次数超过3次,if条件为真,会打印输入次数过多的信息并退出程序,sys.exit(2)是退出代码,2是错误码;如果此时尝试次数不超过3次,本次while循环结束,但没有退出while循环,继续从头开始while循环.
            print("输入必须为正整数,请重新输入!")
            AttemptCount += 1
        else:
            break                                             #如果输入值正常,结束循环,程序继续执行
    except ValueError:                                  #捕获到输入不是整数的异常,程序继续执行
        AttemptCount += 1
        print("输入的不是整数,请重新输入!")
    except Exception as e:                           #捕获到其他异常,程序退出,sys.exit(1)是退出代码,1是错误码
        print(f"发生未知错误:{e},程序退出!")
        sys.exit(1)
    if AttemptCount >= MaxInputCount:     #判断尝试次数是否超过最大值
        print("输入错误次数过多，程序退出!")
        sys.exit(2)
# 调用函数,打印斐波那契数列
if len_f > 0:
    print(f"斐波那契数列的前{len_f}项为:")
    print_fib(len_f)
"""

"""
# 装饰器和闭包代码练习
def fun_1():                                # 这是需要添加的功能1
    print("这是新功能1")
def fun_2():                                # 这是需要添加的功能2
    print("这是新功能2")

def fun_origin(fn_list):               # 这是装饰函数(存疑),用于将fun_1和fun_2的功能添加进去,形参fn_list(类型为函数列表)用于将新功能fun_1和fun_2作为实参传入(以函数列表形式传入),可以使用*args来接收任意数量的函数参数
    def fun_inner():                     # 这是内函数,也是闭包函数
        print("这是原有功能")
        for fn in fn_list:                 # 遍历传入的函数列表,逐一执行
            fn()                               # 执行列表中的每个函数,fn_list是外函数fun_origin的局部变量(类型为函数列表),通过实参传入
    return fun_inner

fun_new = fun_origin([fun_1,fun_2])       # 调用fun_origin函数,将fun_1,fun_2作为函数列表的值传入,返回fun_inner函数
fun_new()                                               # 调用fun_inner函数,执行新功能fun_1,fun_2
"""

"""
# 语法糖代码练习----单个功能导入的代码实现
def fun_origin(fn):               # 这是装饰函数,也是外函数,形参fn用于将新功能fun_1和fun_2作为实参传入
    def fun_inner():               # 这是内函数,也是闭包函数
        print("这是原有功能")
        fn()                             # 这是外函数fun_origin的局部变量,通过传入实参(这里的实参是函数名,例如fun_1),执行了fun_1(),将fun_1的功能引入了装饰函数
    return fun_inner

@fun_origin                        # 语法糖
def fun_1():                          # 这是需要添加的功能1
    print("这是新功能1")
fun_1()

@fun_origin                        # 语法糖
def fun_2():                          # 这是需要添加的功能2
    print("这是新功能2")
fun_2()
"""

"""
# 语法糖代码练习----多个功能导入的代码实现

def fun_1():                        # 新功能1
    print("这是新功能1")

def fun_2():                        # 新功能2
    print("这是新功能2")

def fun_fac(*fn_tur):                                           # 这是装饰器工厂,可变参数fn_tur作为形参,以函数元组的形式接收外部新功能,在本例中,接收实参fun_1和fun_2
    def fun_origin(fn):                                          # 这是装饰函数,形参fn用来接收原始定义的main_function函数对象(原有功能)
        def fun_inner(*args, **kwargs):                   # 这是内函数,也是闭包函数,用于所有功能的最终实现
            print("更新后(装饰后),系统的功能有:")        # 这是提示,显示更新后的系统的功能
            result = fn(*args, **kwargs)                    # 这里实现系统基础功能,核心代码在这里实际执行,fn现在是最初定义的函数对象main_function,这个函数调用将实现原有功能
            for fn_t in fn_tur:                                    # 这是新功能的实现,以for循环实现,注意,这里引用的是最外层的fn_tur,而不是装饰fun_origin的局部变量fn,这是与语法糖单功能导入或者装饰器/闭包函数的区别
                fn_t()
            return result
        return fun_inner                                         # 这是fun_origin函数的返回值,返回fun_inner,注意缩进,它不是fun_inner函数的返回值
    return fun_origin                                            # 这是fun_fac函数的返回值,返回fun_origin

@fun_fac(fun_1,fun_2)                                      # 语法糖,以函数元组形式将fun_1,fun_2传入fun_fac函数
def main_function():                                          # 这是原始的核心代码,实现基础功能,不允许修改,后续的功能,通过语法糖实现
    print("这是原有功能(核心代码),不允许修改")
    return "核心功能执行完毕!"                              # 返回值用来跟踪核心逻辑执行情况
main_function()

# 代码执行逻辑:
# 1,代码首先执行到@fun_fac(fun_1,fun_2),程序发现了语法糖@fun_fac,将(fun_1,fun_2)这个函数元组作为参数传给形参*fn_tur,执行函数调用fun_fac(fun_1,fun_2),产生了返回值fun_origin函数对象
# 2,def main_function()在定义的时候,main_function这个函数名指向了main_function这个原始函数对象
# 3,Python 解释器会执行一个相当于main_function = fun_origin(main_function)的操作,注意这个表达式中,左侧的main_function是函数名(引用),fun_origin是以main_function为参数的函数,右侧括号中的main_function是最初定义的函数对象
# 4,这个表达式的作用,是让函数名main_function不再指向原来最初定义的函数对象main_function,重新指向fun_origin(main_function)这个函数表达式的返回值,也就是fun_inner这个函数对象;同时,将最初定义的函数对象main_function传给fun_origin的形参fn
# 5,main_function()现在相当于fun_inner(),fun_inner()可以传入可变参数*args和**kwargs,由于main_function()未定义参数,所以传入的参数为空,args是空元组,kwargs是空字典,可变参数设计,让它可以成为通用装饰器函数,可以匹配原始函数的任意参数

"""

"""
# 这是多态性的代码练习
class Animal(object):                               # 定义Animal类,继承自系统类/基类object
    def eat(self):
        print("我会吃东西")
class Dog(Animal):                                  # 定义Dog类,继承自Animal类,是Animal类的子类
    def eat(self):
        print("我会吃屎")
class Cat(Animal):                                   # 定义Cat类,继承自Animal类,是Animal类的子类
    def eat(self):
        print("我会吃老鼠")
def fun_eat(animal_eat):                       # 定义通用接口(函数)fun_eat,形参animal_eat(类型为类名)用于接收传入的类名,在本例中,接收的实参可以是父类Animal,子类Dog和Cat
    obj_eat = animal_eat()                      # 实例化传入的类名,obj_eat在实例化后成为对象
    obj_eat.eat()                                     # 通过实例化后的对象obj_eat调用eat方法
fun_eat(Animal)                                   # 调用函数(接口)fun_eat,将Animal类作为参数传入
fun_eat(Dog)                                       # 调用函数(接口)fun_eat,将Dog类作为参数传入
fun_eat(Cat)                                        # 调用函数(接口)fun_eat,将Cat类作为参数传入
# 以上代码,实现了统一的接口调用(fun_eat函数),根据不同的传入参数,实现了方法调用的多态性
"""

"""
# 魔法方法和单例模式练习
class Singleton(object):
    _instance = None                                           # 类属性,用于储存单例对象的引用
    def __new__(cls, *args, **kwargs):                   # 魔法方法__new__()继承自父类object的魔法方法object.__new__(),用于创建Singleton类的实例,cls是类本身,在这里指Singleton类,对__new__()这个魔法方法进行重写,用来实现单例模式的功能
        if not Singleton._instance :                         # 如果类属性_instance为空,说明还没有实例化对象
            Singleton._instance = super().__new__(cls)     # 调用Singleton的父类object类的魔法方法__new__(),这个魔法方法的返回值是新创建的实例的引用,将其赋值给类属性_instance,_instance指向新创建的实例对象,成为这个单例对象的引用
        return Singleton._instance
si = Singleton()                                              # 对Singleton类进行实例化,创建单例对象si
print("这是单例对象si的地址:", id(si))               # 输出单例对象si的地址,用于验证单例模式
si_2 = Singleton()                                          # 对Singleton类进行实例化,创建单例对象si_2
print("这是单例对象si_2的地址:", id(si_2))        # 输出单例对象si_2的地址,用于验证单例模式

"""

"""
# 文件操作代码练习
import os                                                                   # os模块提供了与操作系统交互的功能,可以用于文件和目录操作
file_test = open("test.txt", "w",encoding = "utf_8")    # 打开文件test.txt,以写入模式打开,如果文件不存在,则创建文件
file_test.write("这是天上人间一号妹妹的测试文本!\n")    # 写入内容到文件中
file_test.close()                                                            # 关闭文件,释放资源
os.remove("test.txt")                                                   # 删除文件,释放资源,要查看test.txt,需要先注释本行,否则会删除文件
# 通常,with open() as file是更推荐的写法,它自带文件关闭功能,不需要手动调用close()方法,其函数参数与open()函数相同
"""

"""
# 迭代器和生成器代码练习
from _collections_abc import Iterable,  Iterator
str_1 = "天上人间一号妹妹"
print(isinstance(str_1, Iterable))           # 检查字符串是否可迭代,返回True
print(isinstance(str_1, Iterator))           # 检查字符串是否是迭代器,返回False
print(dir(str_1))                                    # 查看属性str_1的所有属性和方法
str_2 = iter(str_1)                                 # 将字符串转换为迭代器对象,注意,str_2不再是字符串类型,而是迭代器类型
print(isinstance(str_2, Iterable))           # 检查迭代器是否可迭代,返回True
print(isinstance(str_2, Iterator))           # 检查迭代器是否是迭代器,返回True
print(dir(str_2))                                    # 查看迭代器str_2的所有属性和方法
# 通过以上代码,可以看出,字符串是可迭代对象,但不是迭代器对象
# 通过iter()函数,可以将可迭代对象转化为迭代器对象
# 通过查看可迭代对象和迭代器对象的所有属性和方法,迭代器对象比可迭代对象对了__next__()方法
"""

"""
# 生成器代码练习
li = []
n = int(input("请输入生成器的长度:"))  # 接收用户输入的生成器长度
def gen(n):                                         # 这是一个生成器函数
    for i in range(n):
        yield i * i                                     # 使用yield关键字返回生成器对象,每次调用next()方法时,会从上次yield的位置继续执行,直到遇到下一个yield或函数结束
g = gen(n)                                          # 创建生成器对象g,注意,调用生成器函数gen(n)不会立即执行函数体,而是返回一个生成器对象,这是它和普通函数的区别,在本例中,这个赋值表达式使g成为这个生成器对象的引用
for i in g:                                             # 遍历生成器对象g,每次迭代会调用一次生成器函数gen(n)--调用逻辑在下面的注释中,并返回一个值,注意:生成器函数是一种特殊的迭代器对象,而迭代器对象是一种特殊的可迭代对象,所以可以使用for循环遍历生成器对象
    li.append(i)                                     # 将生成器返回的值添加到列表li中
print(f"生成器的长度为:{n},生成器内容列表为:{li}")  # 打印生成器的长度和内容

# 调用生成器函数gen(n)不会立即执行函数体,而是返回一个生成器对象,这是它和普通函数的区别,也是理解代码逻辑的关键所在
# 在for i in g这行代码中,只是对g这个生成器对象进行了遍历取值,没有任何显示的执行或者调用行为,python解释器会发现g是一个迭代器对象,会隐式地调用这个迭代器对象g的 __next__()方法,从而唤醒生成器函数gen(n)的执行,这是python解释器的内部逻辑,是迭代协议的功能,这个语法糖使得代码更简洁,但也让初学者难以理解,因为它隐藏了生成器函数的执行细节
# 假设输入的是3,代码首先执行到g = gen(n),此时并没有执行生成器函数gen(n),而是返回一个生成器对象g,这个对象是一个迭代器对象,它实现了迭代协议,可以被for循环遍历
# 当执行到for i in g时,python解释器会隐式地调用g的__next__()方法,从而唤醒生成器函数gen(n)的执行,第一次执行到yield i * i时,返回0,将0赋值给i
# 然后继续执行下一次迭代,第二次执行到yield i * i时,返回1,将1赋值给i
# 然后继续执行下一次迭代,第三次执行到yield i * i时,返回4,将4赋值给i
# 然后继续执行下一次迭代,此时已经没有更多的值可供返回了,所以抛出StopIteration异常,for循环自动捕获这个异常并结束循环
"""

