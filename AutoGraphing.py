#coding=utf-8
import os

from math import exp
from numpy import array, arange
from seaborn import color_palette
from colorsys import rgb_to_hsv, hsv_to_rgb

import pandas as pd
import matplotlib.pyplot as plt

# Matplotlib 设置
plt.rcParams['font.sans-serif'] = ['simhei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.autolimit_mode'] = 'round_numbers'
plt.rcParams['lines.linewidth'] = '3'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

### 颜色 ####
def rgb2hsb(rgb):   # 转为 HSB 色值
    rgb = (int(rgb[1:3], 16), int(rgb[3:5], 16), int(rgb[5:], 16))
    hsv = rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    return hsv

def hsb2rgb(h, s, b):   # 转回 RGB 色系
    rgb = hsv_to_rgb(h, s, b)
    rgb = '#' + hex(int(rgb[0] * 255))[2:] + hex(int(rgb[1] * 255))[2:] + hex(int(rgb[2] * 255))[2:]
    return rgb  # 一个带#号的字符串

# 生成相邻色
def neighborcolor(rgb, num=2, to='+'): 
    hsb = rgb2hsb(rgb)
    nc_hsb = [hsb]

    for i in range(1, num):
        if to == "+":
            h = nc_hsb[-1][0] + 1 / num
            if h > 1:
                h -= 1
        else:
            h = nc_hsb[-1][0] - 1 / num
            if h < 1:
                h += 1
        nc_hsb.append([h, hsb[1], hsb[2]])
    
    nc_rgb = []
    for color in nc_hsb:
        nc_rgb.append(hsb2rgb(color[0], color[1], color[2]))

    return nc_rgb

# 生成递进色
def degreecolor(base, mode='light', num=3):
    return color_palette(mode + ':' + base + '_r', num)

gray = '#d8d8d8'
black = '#000000'

### 绘图 ####
def FormatTicks(ax, string='{:,}', unit=1):
    y1 = ax.get_yticks()
    y2 = []

    for raw in y1:
        if ',' in string:
            a = int(raw / unit)
        else:
            a = raw / unit
        y2.append(string.format(a))
    
    ax.set_yticks(y1, y2)
# 定义柱和线类
class Bar():
    def __init__(self, num, bottom=0, color='', label=''):
        self.num = num
        self.bottom = bottom
        self.color = color
        self.label = label
class Line():
    def __init__(self, num, color='', label='', ls='-'):
        self.num = num
        self.color = color
        self.label = label
        self.ls = ls

# 画图
def GraphingII(artist, ax, x, width):
    if artist.color == '':
        if isinstance(artist, Bar):
            return (ax.bar(x, artist.num, width, artist.bottom), artist.label)
        elif isinstance(artist, Line):
            return (ax.plot(x, artist.num, ls=artist.ls)[0], artist.label)
    else:
        if isinstance(artist, Bar):
            return (ax.bar(x, artist.num, width, artist.bottom, color=artist.color), artist.label)
        elif isinstance(artist, Line):
            return (ax.plot(x, artist.num, ls=artist.ls, color=artist.color)[0], artist.label)

def GraphingI(list, ax, xlist, hor):
    artists = []
    # 1. 区分Bar 和 Line
    bar_list = []
    line_list = []
    for i in list:
        if isinstance(i, Bar):
            bar_list.append(i)
        elif isinstance(i, Line):
            line_list.append(i)
    bl = len(bar_list)
    # 2. 总宽度和宽度
    if bl == 0 or hor == False:
        width = 0.54
    else:
        width = (0.34 / (1 + exp(-bl + 3)) + 0.5) / bl

    # 3. 设置x 轴
    if hor and bl > 1:
        # 有多个横向的柱子
        xint = arange(len(xlist))
        for i in range(bl):
            if bl % 2 == 0:
                div = (- (bl / 2 - 0.5) + i) * width
            else:
                div = (- (bl / 2 - 1.0) + i) * width
            artists.append(GraphingII(bar_list[i], ax, xint + div, width))
        ax.set_xticks(xint, xlist)
    else:
        for bar in bar_list:
            artists.append(GraphingII(bar, ax, xlist, width))
    # 画折线
    for line in line_list:
        artists.append(GraphingII(line, ax, xlist, width))
    
    artists = array(artists, dtype=object).T.tolist()   
    return artists

def Graphing(major_list, format='{:,}', unit=1, minor_list=[], xlist='', hor=False, **minor_args):
    # Part2: 画图
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    handles = []
    labels = []
    # 主坐标轴
    major = GraphingI(major_list, ax, xlist, hor)
    handles += major[0]
    labels += major[1]
    ax.margins(x=0.05)

    if 'ma_ylim_l' in minor_args.keys():
        ax.set_ylim(minor_args['ma_ylim_l'])
    if 'ma_ylim_u' in minor_args.keys():
        ax.set_ylim(top=minor_args['ma_ylim_u'])
    if ax.get_ylim()[0] * ax.get_ylim()[1] < 0:
        ax.axhline(color='black', lw=1)

    FormatTicks(ax, string=format, unit=unit)
    # 次坐标轴
    if len(minor_list) >= 1:
        ax1 = ax.twinx()
        minor = GraphingI(minor_list, ax1, xlist, hor)
        handles += minor[0]
        labels += minor[1]
        ax1.spines['right'].set_visible(True)   
        ax1.margins(x=0.05)
        if 'mi_ylim_l' in minor_args.keys():
            ax1.set_ylim(minor_args['mi_ylim_l'])
        if 'mi_ylim_u' in minor_args.keys():
            ax1.set_ylim(top=minor_args['mi_ylim_u'])
        if ax1.get_ylim()[0] * ax1.get_ylim()[1] < 0:
            ax1.axhline(color='gray', lw=1, ls='--')
        
        if 'minor_f' not in minor_args.keys():
            minor_args['minor_f'] = '{:,}'
        if 'minor_u' not in minor_args.keys():
            minor_args['minor_u'] = 1
        FormatTicks(ax1, string=minor_args['minor_f'], unit=minor_args['minor_u'])
    # 图例
    plt.legend(handles, labels)
    # 其他设置
    
    if 'save' in minor_args.keys():
        fig.savefig(minor_args['save'])
