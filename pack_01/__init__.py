print("看到这个提示,说明你执行到了__init__.py文件!")

# # 第一种方法:
from. import login # 导入登录模块
from. import register # 导入注册模块

# 第二种方法:
__all__ = ['login', 'register']  # 定义包的公开接口,只导出login和register模块
