# python+CSMAR 自动绘制财务分析图表
## 使用方法
1. 下载脚本和数据  
  - 在CSMAR数据库中下载企业财务报表（资产负债表、利润表和现金流量表），解压后置于同一文件夹
    - 如无特殊要求，下载时勾选所有内容项目为宜  
    - AutoGraphing.ipynb和下载AutoGraphing.py，置于同一文件夹中
2. 基本使用
  - 打开AutoGraphing.ipynb
  - 设置`ID`为分析目标企业代码（写在引号内）
  - 设置`path`为报表Excel文件路径
  - 运行
## 进一步使用
### 颜色
本脚本通过两个内置函数来设置颜色。这些函数都是seaborn包中color_palette函数的特化版本。
- `neighborcolor(rgb, num=2, to='+')`  
  `neighborcolor`为输入的颜色生成`num`个搭配色，并将这些颜色的rgb值以字符串形式存储于一个列表中，列表的第一位是用于生成的基础颜色。  
  根据HSB色彩系统，这些颜色有同样的饱和度（S）和亮度（B），其色相（H）则围绕360°的色轮均匀生成。  
  `to='+'`意味着新生成的颜色，色相会不断增加，直至超过360°之后重新开始；也可以设置`to='-'`，意味着颜色是反向生成的。   
  
- `degreecolor(base, mode='light', num=3)`  
  `degreecolor`生成`num`个更浅/更深(`mode='dark'`)的颜色。  

- 你也可以直接使用color_palette()

### 画图
- 可以使用matplotlib.pyplot画图（已经在AutoGraphing.py中写入）  
  `import matplotlib.pyplot as plt`  

- 使用内置函数`Graphing()`  
  - `major_list`  
    输入一个列表，其中包含有`Bar`和`Line`类  
  - `format='{:,}'`  
    主坐标轴的格式。参考python的`format`函数  
  - `unit=1`  
    主坐标轴的数据单位，支持科学计数法  
  - `minor_list=[]`  
    要绘制在副坐标轴上的`Bar`和`Line`类列表，留空则不画副坐标轴  
  - `xlist=''`  
    x轴上的标签  
  - `hor=False`  
    如果有多个`Bar`类，是堆叠还是并列绘制。默认`horizon=False`即为堆叠
  - `**kwargs`  
    - `ma_ylim_l, ma_ylim_u, mi_ylim_l, mi_ylim_u`  
      设置主(major)、副(minor)坐标轴的上下限  
    - `minor_f, minor_u`  
      设置副坐标轴的格式和单位
    - `save`
      设置图片的保存路径
      
- `Bar`和`Line`类 
  - `Bar`  
    num: 数据列;  
    bottom=0: 底部高度（数据列）;  
    color='': 留空则使用matplotlib自带的色卡;  
    label='': 标签，数据名字
  - `Line`  
    num: 数据列;  
    color='': 留空则使用matplotlib自带的色卡;  
    label='': 标签，数据名字;  
    ls='--': 线的样式
