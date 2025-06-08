# 这是一个通用输入控制模块
import sys  # 导入sys模块
def input_ctrl(max_attempts=3):
    """
    该函数用于控制用户输入,确保用户输入一个非负整数。
    如果用户输入错误,则最多允许max_attempts次尝试,max_attempts默认值为3,如果没有参数传入,限制尝试次数为3。
    如果max_attempts次尝试后仍然输入错误,则程序退出。
    """
    n = 0                                                             # 初始化变量n,用于存储用户输入的非负整数
    count_n = 0                                                  # 初始化计数器变量,用于记录用户输入次数
    while count_n < max_attempts:
        try:
            n = int(input("请输入一个非负整数:")) # 接收用户输入的非负整数
            if n < 0:                                                 # 如果输入的数小于0,则抛出异常
                raise ValueError("输入必须为非负整数")  # 如果执行到这里,说明输入的是负数,抛出异常,break语句不会被执行,因为raise语句会抛出异常,程序会跳转到except语句块
            break                                                    # 如果执行到这里,说明输入有效,跳出while循环
        except ValueError as e:                           # 捕获到输入不是非负整数的异常
            count_n += 1
            if count_n < max_attempts:                # 如果输入次数小于max_attempts,则提示用户重新输入
                print(
                    f"输入错误: {e},请重新输入!")        # 错误被捕获,程序会继续执行,本except块中的代码执行完后,会跳转到while循环的开头,重新执行while循环,直到输入正确或者输入次数超过3次
            else:                                                       # 如果输入次数超过3次,则退出程序
                print("输入错误次数过多,程序退出!")
                sys.exit(1)                                         # 用不同的错误码来区分程序退出的原因,错误码"1"代表输入错误次数过多
        except Exception as e:                            # 捕获其他异常
            count_n += 1                                       # 这里依然记录输入次数,不影响程序逻辑,用于跟踪计数器变量的变化情况
            print(f"发生未知错误: {e},程序退出!")
            sys.exit(2)                                             # 用不同的错误码来区分程序退出的原因,错误码"2"代表未知错误
    return n  # 返回用户输入的非负整数