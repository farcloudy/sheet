# sheet
python+CSMAR 自动绘制财务分析图表

下载AutoGraphing.ipynb并运行

文件依赖：从Csmar数据库下载的财务报告数据

核心函数：  
`
Graphing():
  major_list  一个列表，里面放置Bar和Line类
  format      格式化字符串代码，用于定义主要纵坐标轴格式，默认为'{:,}'（千分位符）
              注：若使用千分位符，会自动调整为int格式
  unit        主要纵坐标轴显示单位，默认为1
  minor_list  放置显示在副坐标轴上的绘图内容
  xlist       x坐标轴的显示元素（列表、array、Data series等）
  hor         是否让多个柱状图Bar元素并列显示，默认为FALSE（堆叠）
  **kwargs
    ma_ylim_l, ma_ylim_u, mi_ylim_l, mi_ylim_u
      设置主、副坐标轴上下限; 
      u: upper, 上限; l: lower, 下限
      ma>major; mi: minor
    minor_f, minor_u:
      副坐标轴格式和单位
    save:
      保存路径
####################
Bar类:
  num     要绘制柱状图的数据
  bottom  底部高度，默认为0
  color   字符串rgb颜色，留空则使用matplotlib默认色板
  label   标签
Line类:
  num     要绘制折线图的数据
  color   字符串rgb颜色，留空则使用matplotlib默认色板
  label   标签
  ls      线的样式
####################
neighborcolor():
  rgb   默认颜色
  num   生成几个相邻色，函数最后返回默认色+所有相邻色的列表
  to    在调色板上顺序取色还是逆序取色，默认为顺序
  seaborn包的color_palette函数支持在360°HSB颜色体系上均匀选择任意个颜色，但是起点是固定的。这个函数使得用户可以指定起点
degreecolor()
  封装了一下color_palette的light / dark模式
`
