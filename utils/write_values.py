#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'


##之前的write_ki是修改的每一行的第二个数，现在改变思路，直接生成要输入的值，一下子覆盖进去
def write_ki(Nod_num,para,i):
    value_list={}   #产生要添加的ki序列
    args_ki=r'E:\EnKF_Gas_Modelling\gas_{0}\gas_KI.direct'.format(i)
    for i in xrange(Nod_num):
        value_list[i]=para[i]
    value_list_to_str=[]    #将序列转换成可以写入文件的字符串格式
    for i,j in value_list.iteritems():
        var=' '.join([str(i),str(j),'\n'])  #使用join进行字符串的拼接效率更高
        value_list_to_str.append(var)
    with open(args_ki,'w') as f:
        for line in value_list_to_str:
            f.write(line)
            pass
        f.write('#STOP')


# 定义函数，将更新之后的p1的值写入direct文件
def write_p1(Nod_num,p1,i):
    value_list={}   #产生要添加的p1序列
    args_p1=r'E:\EnKF_Gas_Modelling\gas_{0}\gas_PRESSURE1.direct'.format(i)
    for i in xrange(Nod_num):
        value_list[i]=p1[i]
    value_list_to_str=[]    #将序列转换成可以写入文件的字符串格式
    for i,j in value_list.iteritems():
        var=' '.join([str(i),str(j),'\n'])
        value_list_to_str.append(var)
    with open(args_p1,'w') as f:
        for line in value_list_to_str:
            f.write(line)
            pass
        f.write('#STOP')