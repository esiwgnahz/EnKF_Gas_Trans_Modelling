#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'
import numpy as np
import os
from utils.generateL import generateL
root_directory=r'E:\EnKF_Gas_Modelling\true_obs'
Nod_num=1681


##负责将参数写入tec文件，查看pattern是否合理
def para_distribution_map(para,Nod_num,root_directory):
    file_name='parameter_distribution.tec'
    args_tec=os.path.join(root_directory,file_name)
    with open(args_tec,'r') as f:
        content=f.readlines()
        content_modify=content[3:3+Nod_num]    #3是tec文件的头部行数

    for i in range(len(para)):
        line=content_modify[i]
        line=line.split()
        line[3]=str(para[i])
        content_modify[i]=' '.join(line[m] for m in range(len(line)))+'\n'
        content[i+3]=content_modify[i]

    with open(args_tec,'r+') as f:
        for line in content:
            f.write(line)


