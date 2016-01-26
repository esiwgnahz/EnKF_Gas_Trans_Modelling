#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'

import pandas as pd
import numpy as np

##定义函数，读取观测点处对应的预测值
def read_obs(Nod_num,obs_Num,i):
    args_obs=r'E:\EnKF_Gas_Modelling\gas_{0}\gas_domain_AIR_FLOW_quad.tec'.format(i)
    with open(args_obs,'r') as f:
        Nod_inf=f.readlines()
    last=Nod_inf[-(1600+Nod_num):-1600]  #1600是elements的个数
    for i in xrange(Nod_num):
        last[i]=last[i].split()
    last=pd.DataFrame(last)
    obs_prediction=last.ix[obs_Num,[3]]
    obs_prediction=obs_prediction.values
    obs_prediction=np.float64(obs_prediction)
    obs_p1=obs_prediction[:,0]
    return obs_p1


##读取所有的p1值
def read_p(Nod_num,i):
    p_result=r'E:\EnKF_Gas_Modelling\gas_{0}\gas_domain_AIR_FLOW_quad.tec'.format(i)
    with open(p_result,'r') as f:
        Nod_inf=f.readlines()
    last=Nod_inf[-(1600+Nod_num):-1600]
    head=[None]*Nod_num
    for i in xrange(len(last)):
        line=last[i].split()
        head[i]=line[3:4]

    head=np.array(head)
    head=np.float64(head)
    return head