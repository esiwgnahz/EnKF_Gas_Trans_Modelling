#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'

import os
import numpy as np
import pandas as pd

from utils.generateL import generateL

def para_init(sigma,deltax,deltay,dx,dy,m,n,Nod_num,N,ki_mean):
    L1=generateL(sigma,deltax,deltay,dx,dy,m,n)
    ran=np.random.standard_normal((Nod_num,N))   ##如果是产生真实参数场的话，那么这里的N就是1
    lnpara=np.dot(L1,ran)
    mean=np.log(ki_mean)
    lnpara=lnpara+mean
    np.savetxt('para_initial.txt',lnpara)
    return lnpara

##计算初始样本的spread
def spread_calculation():
    args=r'E:\EnKF_Gas_Modelling\para_initial.txt'
    content=pd.read_csv(args,sep=' ',names=[i for i in range(100)])
    content=content.values
    var=np.var(content,axis=1)
    std=np.sqrt(np.mean(var,axis=0))
    return std

if __name__=='__main__':
    y=spread_calculation()
    print y





