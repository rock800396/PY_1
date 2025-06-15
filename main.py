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
for i in g:                                            # 遍历生成器对象g,每次迭代会调用一次生成器函数gen(n)--调用逻辑在下面的注释中,并返回一个值,注意:生成器是一种特殊的迭代器对象,而迭代器对象是一种特殊的可迭代对象,所以可以使用for循环遍历生成器对象
    li.append(i)                                     # 将生成器返回的值添加到列表li中
print(f"生成器的长度为:{n},生成器内容列表为:{li}")  # 打印生成器的长度和内容

# 调用生成器函数gen(n)不会立即执行函数体,而是返回一个生成器对象,这是它和普通函数的区别,也是理解代码逻辑的关键所在
# 在for i in g这行代码中,只是对g这个生成器对象进行了遍历取值,没有任何显式的执行或者调用,python解释器会发现g是一个生成器器对象,会隐式地调用这个生成器对象g的 __next__()方法,从而触发生成器函数gen(n)的执行,这是python解释器的内部逻辑,是迭代协议的功能,这个语法糖使得代码更简洁,但也让初学者难以理解,因为它隐藏了生成器函数的执行细节
# 假设输入的是3,代码首先执行到g = gen(n),此时并没有执行生成器函数gen(n),而是返回一个生成器对象g,这个对象是一个生成器对象,它实现了迭代协议,可以被for循环遍历
# 当执行到for i in g时,python解释器会隐式地调用g的__next__()方法,从而唤醒生成器函数gen(n)的执行,第一次执行到yield i * i时,返回0,将0赋值给i
# 然后继续执行下一次迭代,第二次执行到yield i * i时,返回1,将1赋值给i
# 然后继续执行下一次迭代,第三次执行到yield i * i时,返回4,将4赋值给i
# 然后继续执行下一次迭代,此时已经没有更多的值可供返回了,所以抛出StopIteration异常,for循环自动捕获这个异常并结束循环
"""

"""
# 主程序入口的最佳实践和内部逻辑
# if __name__ == "__main__"                               # 主程序入口的最佳实践,用于判断当前模块是否是主程序入口,如果是,则执行主程序逻辑;如果不是,则不执行主程序逻辑

# 每一个py文件,都有一个__name__属性,平时,__name__保存的是自己的模块名(py文件名),例如,py_1.py这个模块中,__name__属性在平时的时候值为"py_1",但是当py_1.py被直接运行时,python解释器会把__name__属性赋值为"__main__"
# 因此,当py_1.py被直接运行时,由于__name__被赋值为"__main__",所以if __name__ == "__main__"这个表达式的值为真,主函数的程序逻辑启动;
# 而当py_1.py被作为模块导入时,由于__name__的值为"py_1",所以if __name__ == "__main__"这个表达式的值为假,主函数的程序逻辑不会启动.
# 这种设计的好处是,可以在一个py文件中既包含可执行的主程序逻辑,又可以包含可供其他模块导入的函数和类定义,从而实现代码的复用和模块化设计.

# 多线程代码练习
import threading                            #导入线程模块
import time                                    #导入时间模块,用于模拟线程执行时间
def fun_1():                                    # 线程1的函数
    print("线程1开始执行")
    time.sleep(2)
    print("线程1执行到一半")
    time.sleep(2)
    print("线程1执行完毕")
def fun_2():                                    # 线程2的函数
    print("线程2开始执行")
    time.sleep(1.5)
    print("线程2执行到一半")
    time.sleep(1.5)
    print("线程2执行完毕")

if __name__ == "__main__":                                # 主程序入口,本例中并无实际意义,只是为了演示主程序入口的最佳实践,养成良好的编程习惯
    thread_1 = threading.Thread(target=fun_1)  # 创建线程1,指定执行的函数为fun_1
    thread_2 = threading.Thread(target=fun_2)  # 创建线程2,指定执行的函数为fun_2
    thread_1.start()                                  # 启动线程1
    thread_2.start()                                  # 启动线程2
    thread_1.join()                                   # 阻塞进程,线程1执行完毕后,主线程才会继续执行
    thread_2.join()                                   # 阻塞进程,线程2执行完毕后,主线程才会继续执行
    print("所有线程执行完毕")                   # 所有线程执行完毕后,打印提示信息,如果没有join()方法,这一行会在子线程执行完之前被打印出来(注释掉上面两行阻塞进程就可以观察到结果)

# 如果设置守护进程thread_1.setDaemon(True)和thread_2.setDaemon(True),主线程执行结束后,子线程会被强制终止,无法看到两个子进程执行的结果
# 注意,守护进程必须放在start()方法之前,而阻塞进程join()方法必须放在start()方法之后
# 如果线程函数fun_1()带参数,可以在创建线程时进行指定,格式为:thread_1 = threading.Thread(target=fun_1,args=(1,2)),这里需要注意的是,参数是以元组形式传入,如果只有一个参数,需要在元组中加上逗号,例如:thread_1 = threading.Thread(target=fun_1,args=(1,))
"""

"""
# 多线程资源竞争的代码练习
import threading
lock = threading.Lock()
a = 0
b = 5000000
def add_1():
    global a
    lock.acquire()
    for i in range(b):
        a += 1
    print(f'第一次累加的结果为：{a}')
    lock.release()
def add_2():
    global a
    lock.acquire()
    for i in range(b):
        a += 1
    print(f'第二次累加的结果为：{a}')
    lock.release()
if __name__ == "__main__":
    thread_1 = threading.Thread(target=add_1)
    thread_2 = threading.Thread(target=add_2)
    thread_2.start()
    thread_1.start()
    # thread_1.join()
    # thread_2.join()
    # print(f'程序结束时全局变量a的最终值：{a}')
"""

"""
# 进程间不共享全局变量演示
from multiprocessing import Process
li = []                                                                                  # 引入全局变量li,初始值为空,列表类型
def fun_write(lof_li):                                                           # 对列表进行写操作
    for i in range(lof_li):
        li.append(i)
    print("这是写入的列表",li)
def fun_read():                                                                   # 对列表进行读操作
    print("这是读取到的列表",li)
if __name__ == "__main__":                                                # 设置主程序入口,本例中并无实际意义,只是为了养成良好的编程习惯
    len_of_li = int(input("请输入列表的长度:"))                         # 控制列表长度
    process_1 = Process(target=fun_write,args=(len_of_li,))   # 创建进程process_1,指定执行的函数为fun_write,将用户输入的长度参数(实参len_of_li)传给
    process_2 = Process(target=fun_read)                            # 创建进程process_2,指定执行的函数为fun_read
    process_1.start()                                                             # 启动进程process_1
    process_1.join()                                                              # 阻塞进程,等待进程process_1执行完毕后,主进程才会继续执行,此处用于表示:即使执行写操作的process_1进程执行结束,后续的process_2依然无法读取到process_1写入全局变量li中的数据,这表明process_1和process_2不共享全局变量li
    process_2.start()                                                             # 启动进程process_2
"""

"""
# queue队列实现进程间通信代码练习
from multiprocessing import Process,Queue                      # 这里需要注意,这种方式导入的Q队列用于进程间通信(开销更大,效率更低),如果是以from queue form Queue方式导入,则用于线程间通信(效率更高,但不能用于进程间通信)
li = []                                                                                 # 引入全局变量li,初始值为空,列表类型
q = Queue()                                                                       # 引入全局变量q,初始值为空,队列类型,用于进程间通信
def fun_write(q_1):
    for i in range(10):
        li.append(i)                                                                # 向列表中添加数据,用于展示列表中有多少数据需要传到另一个进程process_2中
        q_1.put(i)                                                                   # 向列表中添加的数据,同时也用put方法传到队列q_1中,用于进程间通信
    print("这是进程process_1生成的列表,需要传到进程process_2中",li)
    q_1.put(None)                                                               # 产生一个哨兵值,用于让process_2进程中知道数据已经传完了
def fun_read(q_2):
    while True:
        item = q_2.get()                                                        # 尝试获取数据，如果队列为空会阻塞
        if item is None:                                                         # 检查是否是哨兵值,如果是,代表数据已经传完了,退出循环
            break
        else:
            li.append(item)
    print("这是从进程process_1中通过Q队列传过来的数据",li)
if __name__ == "__main__":                                                # 设置主程序入口,本例中并无实际意义,只是为了养成良好的编程习惯
    process_1 = Process(target=fun_write,args=(q,))            # 创建进程process_1,指定执行的函数为fun_write,将实参q传给q_1,q_1成为队列类型,这个q_1只在进程process_1中使用
    process_2 = Process(target=fun_read,args=(q,))             # 创建进程process_2,指定执行的函数为fun_read,将实参q传给q_2,q_2成为队列类型,这个q_2只在进程process_2中使用
    process_1.start()                                                             # 启动进程process_1
    process_2.start()
    process_1.join()                                                              # 这里需要注意,之所以没有将这一行放在process_2.start()前面,是因为process_2进程中get()方法会默认阻塞,不会因为没有process_1.join() 而无法获取到数据,这和上一个"进程间不共享全局变量演示"中是不一样的
    process_2.join()

 # multiprocessing.Queue 的核心原理：
 # q, q_1, q_2 等 Queue 对象,虽然在各自进程中是独立的Python实例,由于进程之间资源不共享而无法直接通信
 # 但它们都作为代理/句柄,指向并操作着同一个由操作系统管理的底层进程间通信(IPC)通道(如管道)
 # 数据在通过此通道传递时,会被自动序列化和反序列化,从而实现跨进程的通信,即便进程内存是隔离的
"""

"""
# 代码练习1 找出并打印2000-3200之间(包含)能被7整除不能被5整除的数
li = []
for i in range(2000,3201):
    if i%7 == 0 and i%5 != 0:
        li.append(i)
print(f"2000-3200之间能被7整除,但不能被5整除的数有:{li}")
print(f"2000-3200之间能被7整除,但不能被5整除的数有{len(li)}个")
"""

"""
# 代码练习2 计算给定数阶乘
import  sys
n = 0                                                 # 初始化n为0,用于接收用户输入的非负整数
count_n = 0                                      # 限制输入次数为3次
def factorial(n):                                 # 使用递归函数计算阶乘,注意这里的形参n是局部变量,与全局变量n无关,在函数调用时会传入实参,实参的值会覆盖形参的值
    if n == 1 or n == 0:
        return 1
    else:
        return n * factorial(n-1)
if __name__ == "__main__":
    while count_n < 3 :
        try:
            n = int(input("请输入一个非负整数:"))    # 接收用户输入的非负整数
            if n < 0:                                                   # 如果输入的数小于0,则抛出异常
                raise ValueError("输入必须为非负整数")       # 如果执行到这里,说明输入的是负数,抛出异常,break语句不会被执行,因为raise语句会抛出异常,程序会跳转到except语句块
            break                                                                  # 如果执行到这里,说明输入有效,跳出while循环
        except ValueError as e:                             # 捕获到输入不是非负整数的异常
            count_n += 1
            if count_n < 3:                                        # 如果输入次数小于3次,则提示用户重新输入
                print(f"输入错误: {e},请重新输入!")     # 错误被捕获,程序会继续执行,本except块中的代码执行完后,会跳转到while循环的开头,重新执行while循环,直到输入正确或者输入次数超过3次
            else:                                                        # 如果输入次数超过3次,则退出程序
                print("输入错误次数过多,程序退出!")
                sys.exit(1)                                                 # 用不同的错误码来区分程序退出的原因,错误码"1"代表输入错误次数过多
        except Exception as e:                              # 捕获其他异常
            count_n += 1                                         # 这里依然记录输入次数,不影响程序逻辑,用于跟踪计数器变量的变化情况
            print(f"发生未知错误: {e},程序退出!")
            sys.exit(2)                                                     # 用不同的错误码来区分程序退出的原因,错误码"2"代表未知错误
    print(f"{n}的阶乘 {n}! = {factorial(n)}")
"""

"""
# 代码练习3 根据给定正整数n,生成一个{1:1*1, 2:2*2, ..., n:n*n}的字典
from input_ctrl import input_ctrl   # 从外部导入输入控制模块,用于接收用户输入的正整数并进行验证
n = 0                                                 # 初始化n为0,用于接收用户输入的正整数,会以外部函数input_ctrl()的返回值形式传入
dict_n = {}                                         # 初始化一个空字典,用于存储生成的字典
def fun_dict(n):                                 # 生成函数,使用for循环
    for i in range(1,n+1):
        dict_n[i] = i*i
if __name__ == "__main__":
    max_attempts = 5                                              # 设置最大尝试次数为5次,可以按需设置
    n = input_ctrl(max_attempts)                            # 参数可以为空,input_ctrl会使用默认值3
    fun_dict(n)                                                           # 调用函数fun_dict(n),生成字典
    print(f"长度为{n}的字典为{dict_n}:")
"""

# """
# # 代码练习4 使用正则表达式从序列中提取数字,并以默认的列表形式输出
# import re                                         # 导入正则表达式模块
# def ext_num(seq):                           # 定义提取函数ext_num,形参seq用于接收传入的序列
#     pa = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)"                # 定义正则表达式,匹配数字
#     return re.findall(pa,seq)             # 使用re.findall()方法提取序列中的数字,re.findall(pa,seq)的值是一个数字列表,这个列表作为返回值返回给调用者
# if __name__ == "__main__":            # 主程序入口,养成好习惯
#     seq = input("请输入任意一个需要提取的序列")        # 接收用户输入的序列,可以是字符串、列表等,只要能被正则表达式匹配即可
#     print(f"提取到的数字序列为:{ext_num(seq)}")          # 调用提取函数ext_num(seq),提取序列中的数字,并打印输出,这里注意形参和实参使用同一个变量名seq,但实际并不是同一个东西
# """

"""
# 代码练习5 构造一个包含2个方法的类,一个用于获取控制台输入的字符串,另一个用于将字符串转换为大写并打印输出
class StrToUpper(object):                                       # 这是一个包含两个方法的类,一个用于获取控制台输入的字符串,另一个用于将字符串转换为大写并打印输出'
    def __init__(self):
        self.str_input = ""                                             # 初始化一个空字符串,用于存储用户输入的字符串
    def get_input(self):
        self.str_input = input("请输入一个字符串:")     # 获取用户输入的字符串,并存储到实例变量str_input中
    def print_upper(self):
        print(f"转换为大写后的字符串为: {self.str_input.upper()}")  # 将实例变量str_input转换为大写并打印输出
if __name__ == "__main__":                                      # 主程序入口,养成好习惯
    obj = StrToUpper()                                              # 创建StrToUpper类的实例对象obj
    obj.get_input()                                                     # 调用实例方法get_input()获取用户输入的字符串
    obj.print_upper()                                                 # 调用实例方法print_upper()将字符串转换为大写并打印输出
# 执行逻辑:get_input方法获得字符串输入后,将其存储到实例变量str_input中,调用print_upper方法,将str_input转换为大写并打印输出
"""

"""
# 代码练习6 math.sqrt函数的使用
import math                                               # 导入math模块,用于数学计算
a = 50
b = 30
c = []                                                          # 接收外部输入
value = []                                                   # 存储输出数据
for i in input("请输入一组数字,以逗号分隔:").split(","):             # 接收用户输入的数字,以逗号分隔,并将其转换为列表
    c.append(float(i))                                                            # 将输入的数字转换为浮点数,并添加到列表c中
for i in c :
    i = int(math.sqrt(2*a*i/b))                                               # 根据公式计算并将结果转化为int整型
    value.append(i)
print(f"计算结果为:{value}")
"""

"""
# 代码练习7 二维数组的生成
lst = []                                              # 定义一个数组lst,这个数组是一个二维数组,其中的元素是一维数组
def arr(par_1,par_2):                        # 定义数组生成函数,形参par_1和par_2是数组的行和列
    for i in range(par_1):                   # 用循环处理行
        lst.append([])                           # 向二维数组列表lst中添加一个空的一维数组,这个一维数组成为lst[i]
        for j in range(par_2):               # 用循环处理列
            lst[i].append(i*j)                  # 向二维数组列表lst中的元素lst[i]添加j个元素,每个元素的值为i*j,lst[i]成为一个有j个元素的一维数组
        print(f"数组第{i+1}行为:{lst[i]}")      # 这纯粹是为了输出美观,在数组超过一行时,可以直观看到行和列的编号
if __name__ == "__main__":             # 主程序入口,养成好习惯
    arr(10,10)
    print(f"二维数组为:{lst}")
"""

"""
# 代码练习8 对随机输入的单词按字母顺序重排序,输入分隔符为","
# 假设输出字符串为: SVPN,Cherry,Chatbox,VSCode,PyCharm,github,Docker
wor_lst = [x for x in input("请输入一组单词,以逗号分隔:").split(",")]           # 接收用户输入的单词,以逗号分隔,并将其转换为列表
wor_lst.sort()                                                                                                 # 对列表中的单词按字母顺序排序
print(f"按字母顺序排序后的单词列表为:{wor_lst}")                                       # 这种方式输出的是字符串列表,与原格式不同
print(",".join(wor_lst))                                                                                   # 这种方式输出的是字符串,与原格式相同,使用join()方法将列表中的元素连接成一个字符串,以逗号分隔
wor_lst = [x for x in input("请输入一组单词,以逗号分隔:").split(",")]           # 重新接收相同的用户输入,以便形成对比(执行结果相同,但执行过程中wor_lst的值不一样)
# wor_lst.sort(key=str.lower)                                                                       # 这一行会导致类型不匹配警告,用下一行代替
wor_lst.sort(key=lambda x: x.lower())                                                         # 对列表中的单词按字母顺序排序,不区分大小写,使用匿名函数实现
print(f"不区分大小写排序后的单词列表为:{wor_lst}")
print(",".join(wor_lst))
"""

"""
# 代码练习9 接收任意输入序列,并将其中的小写字母转换为大写字母并打印
import  re
seq = input("请输入任意一个需要转换的序列:")          # 接收用户输入的序列
print(f"转换后的序列为: {seq.upper()}")                       # 将输入的序列转换为大写字母并打印输出
pattern = r'[a-zA-Z]'                                                    # 定义一个只匹配字母的正则表达式
matches = re.findall(pattern, seq)                             # 使用re.findall()方法提取序列中的字母,返回一个列表
con = "".join(matches)                                                # 用.join方法将列表中的字母连接成一个字符串,""表示连接符为空,也就是不做分隔
str_up = con.upper()                                                   # 将连接后的字符串转换为大写字母
print(f"仅提取字母并转换为大写: {str_up}")                 # 打印输出转换后的字符串
print(f"仅提取字母并转换为大写: {''.join(re.findall(pattern,seq)).upper()}")          # 这是将多个步骤合并为一行的写法,较为复杂,容易出错
"""

"""
# 代码练习10 删除重复单词(空格分隔)并重排序
# 假设输入序列为: Hello World and hello girl and hello boy and hello man
words = [word for word in input("请输入单词序列:").split(" ")]
print(" ".join(sorted(list(set(words)))))                # set将words列表转换为集合,利用集合的元素唯一性去重;list将集合重新转为列表,因为集合是无序的,不能排序;sorted()是系统自带方法,参数可以是任何可迭代对象,返回值是排序后的对象,原对象不变,这是和列表方式sort()的重要区别;最后," "调用join方法,使用空格将排序后的列表元素(单词)连接起来,保持原来的样式
# words = list(set(words))                                   # 这是另一种方法,使用sort()方法来代替sorted()方法
# words.sort()
# print(" ".join(words))
"""

"""
# 代码练习11 假设输入是以空格分隔的二进制数值序列,检查这些二进制数值是否能被5整除,只保留可以被整除的二进制数值
# 假设输入序列为:1100101 101100 1010 101110 11010011
num_out = []                                                                                                  # 定义一个空列表,用于输出
num = [x for x in input("请输入二进制数值序列,以空格分隔:").split(" ")]                # 接收二进制数值序列并根据空格分隔使用列表生成式将其以列表形式保存到列表num中
for i in num:
    if int(i,2)%5 == 0:                                                                                        # int(i,2)将二进制i转化为10进制整型,2代表i是二进制数值
        num_out.append(i)
# num_out = [x for x in input("请输入二进制数值序列,以空格分隔:").split(" ") if int(x, 2) % 5 == 0]            # 使用带条件的列表推导式,更加简洁优雅,不需要使用for循环,也不需要定义变量,以上5行代码都被这一行取代,初学者可能比较难看懂
print(f"序列中可以被5整除的数值为:"," ".join(num_out))                                      # 通过.join方式将列表num_out中的元素以空格进行连接,使输出格式与输入格式保持一致
"""

"""
# 代码练习12 找到1000到3000之间(包含头尾)所有位数均为偶数的数值,以逗号分隔并打印
pri_lst = []                                        # 初始化一个空列表,用于存储符合条件的数值
for i in range(1000,3001):
    chk = True
    for k in str(i):                                # 内层循环对每一位是否为偶数进行检查
        if int(k) % 2 != 0:
            chk = False                          # 只要有一位是奇数,chk标志将被重置为False
            break
    if chk:                                          # 只有在chk标志为True时才将值添加到列表中,添加前先转化为字符串,便于后续拼接
        pri_lst.append(str(i))
print(f"1000-3000中,所有位数均为偶数的数字有:",",".join(pri_lst))

# # 使用all函数实现的最佳实践版本
# pri_lst = []
# for i in range(1000, 3001):
#     if all(int(k) % 2 == 0 for k in str(i)):
#         pri_lst.append(str(i))
# print(f"1000-3000中,所有位数均为偶数的数字有:",",".join(pri_lst))
"""

# # 代码练习13 统计输入序列中大写字母,小写字母和数字的个数
# # 方法1,使用正则表达式,这种方法在提取的时候更有用,统计时效率不如方法2
# import re
# seq = input("请输入任意序列:")                         # 接收输入序列
# pat_letter_u = r"[A-Z]"                                     # 正则表达式,匹配大写字母
# pat_letter_l = r"[a-z]"                                       # 正则表达式,匹配小写字母
# pat_letter_d = r"[0-9]"                                      # 正则表达式,匹配数字
# print(f"大写字母的个数为:{len(re.findall(pat_letter_u, seq))}")
# print(f"小写字母的个数为:{len(re.findall(pat_letter_l, seq))}")
# print(f"数字的个数为:{len(re.findall(pat_letter_d, seq))}")

# #方法2,使用isupper,islower,isdigit方法实现
# seq = input("请输入任意序列:")
# num_up = 0
# num_low = 0
# num_dig = 0
# for i in seq:
#     if i.isupper():
#         num_up += 1
#     if i.islower():
#         num_low += 1
#     if i.isdigit():
#         num_dig += 1
# print(f"大写字母的个数为:{num_up}\n小写字母的个数为:{num_low}\n数字的个数为:{num_dig}")

# 代码练习15 给定一个范围在1-9的正整数a,计算算式a+aa+aaa+...的值,算式的项数为n,a和n通过形参赋值
# def fun_count(a,n):                                           # 注意,这里没有对a和n的取值范围做判断,实际中是不合适的
#     if n == 0:                                                      # 如果算式项数为0,无论a是什么值都是空算式
#         return 0
#     else:
#         return a + fun_count(a*10,n-1)                 # 计算第n项的值,这个递归函数的设计是难点,可以考虑使用for循环来实现
# if __name__ == "__main__":
#     a = 4                                                            # a和n的值作为实参传入fun_count()函数,通过改变a和n的值来改变算式
#     n = 9
#     # 实现方法1如下
#     result = 0
#     for i in range(1,n+1):
#         result += fun_count(a,i)
#     print(f"计算结果为:{result}")
#     # 实现方法2如下
#     result = sum(fun_count(a, i) for i in range(1, n + 1))          #更高效的方法,使用了内置函数sum
#     print(f"计算结果为:{result}")

# 代码练习-网络爬虫-1
import requests
import re
import sys
pattern = r'^(https?://)?([a-zA-Z0-9.-]+)(:[0-9]+)?(/.*)?$'                                                                                     # 检查网址合法性的正则表达式,全局变量
IP_PATTERN = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'      # 检查IP地址合法性的正则表达式,只支持IPv4地址
if __name__ == "__main__":                                                             # 主程序入口
    while True:                                                                                    # 使用while循环,直到用户输入合法的URL
        try:
            url = input("请输入需要爬取的URL:")                                           # 接收用户输入的URL
            if re.match(pattern, url) is None:                                                # 如果网址不合法,则抛出异常
                raise ValueError("输入的网址不合法,请检查后重新输入!")       # 抛出异常,提示用户输入的网址不合法,会跳转到except语句块
            response = requests.get(url)                                                       # 使用requests库发送GET请求,获取网页内容
            print(f"获取的请求内容为:\n{response.text}")                              # 打印获取的网页内容,换行只是为了美观
            break                                                                                             # 如果获取成功,则跳出while循环,否则会陷入死循环
        except ValueError as e:                                                                    # 捕获异常
            print(f"发生错误: {e}")                                                                    # 打印异常信息
        except Exception as e:                                                                      # 捕获其他异常
            print(f"发生未知错误: {e}")                                                             # 打印异常信息
            sys.exit(2)                                                                                      # 退出程序,错误码为2用来跟踪未知错误