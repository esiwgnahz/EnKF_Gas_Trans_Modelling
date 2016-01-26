#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'
import os
root_directory=r'C:\Users\zq\Desktop\true_obs_gas'
##该函数实现的功能是自由地往gli文件中添加观测点，基础点共有8个，所以新加入点的编号从8开始往后编，见key_num
##修改参数文件的思路是先将文件读取出来，加入或修改新增的内容，再将修改后的内容写进原文件

def modify_gli(num,root_directory):
    #第一部分实现了新加入点的绘制,num是基础几何的坐标点的个数
    cor={}
    key=0
    for i in xrange(25,225,50):   #这里的i,j是为了定位新增点的坐标
        for j in xrange(2,10,2):
            cor[key]='{a} {b}'.format(a=i/100.0,b=j/10.0)
            key+=1
    cor=cor.values()
    cor_add={}
    key_add=0
    for i,cor1 in enumerate(cor):   #修改成与原文件中坐标点一样的格式
        cor1=cor1.split()
        cor1.insert(1,'0')
        key_num=str(i+num)    #这里的num是基础几何的坐标点的个数，因此新增点的编号从num开始
        cor1=key_num+' '+cor1[0]+' '+cor1[1]+' '+cor1[2]+' \n'
        cor_add[key_add]=cor1
        key_add+=1
    cor_add=cor_add.values()

    #第二部分实现了新增点的加入以及写入gli文件
    file_name='gas.gli'
    args=os.path.join(root_directory,file_name)
    f=open(args,'r')
    content=f.readlines()
    f.close()
    for i in range(len(cor_add)):
        content.insert(num+1+i,cor_add[i])
    f=open(args,'w')
    for line in content:
        f.write(line)
    f.close()

if __name__=='__main__':
    modify_gli(10,root_directory)