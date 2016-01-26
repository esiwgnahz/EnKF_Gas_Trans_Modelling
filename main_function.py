#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'


import math
from math import e
import numpy as np
import random as rd
import pandas as pd
import matplotlib.pyplot as plt
import win32api
import time
import os
from utils.generateL import generateL
from gevent import pool
from utils.generate_obs import generate_obs
from utils.values_init import para_init
from utils.para_key_mod import para_keys_modify
from utils.write_values import write_ki,write_p1
from utils.read_values import read_obs,read_p
from utils.time_modify import time_modify

time_step=20
Nod_num=1681
N=100
varR=80
obs_Num=[213,221,229,237,623,631,639,647,1033,1041,1049,1057,1443,1451,1459,1467]
obs_num=len(obs_Num)
sigma=0.9
ki_mean=2.9e-15
deltax=1
deltay=0.5
dx=0.05
dy=0.025
x=2
y=1
m=int(y/dy+1)
n=int(x/dx+1)
root_directory=r'E:\EnKF_Gas_Modelling'
root_directory_true_obs=r'E:\EnKF_Gas_Modelling\true_obs'


##调取观测值样本
obs_Pressure1=generate_obs(time_step,obs_num,varR,N,root_directory_true_obs)
t=1
y_p1=obs_Pressure1[t]
y_obs_p1=pd.DataFrame(y_p1)
y_obs_p1=y_obs_p1.T
y_obs_p1=y_obs_p1.values

y_obs_prediction=np.zeros([obs_num,N])
p_after=np.zeros([Nod_num,N])

#产生初始p1
p1_initial=np.zeros([Nod_num,N])
p1_initial=p1_initial+101325

#产生初始参数
para_initial=para_init(sigma,deltax,deltay,dx,dy,m,n,Nod_num,N,ki_mean)
np.savetxt('para_initial.txt',para_initial)
ki_initial=np.exp(para_initial)


def runexe(ki_initial,pi_initial,i):
    args_exe=r'E:\EnKF_Gas_Modelling\gas_{0}\ogs.exe'.format(i)
    args=r'E:\EnKF_Gas_Modelling\gas_{0}'.format(i)
    ki_modify=ki_initial[:,i]
    ki_modify=para_keys_modify(ki_modify)
    write_ki(Nod_num,ki_modify,i)  #para为初始参数，样本之间存在随机扰动
    write_p1(Nod_num,p1_initial[:,i],i)
    win32api.ShellExecute(0,'open',args_exe,'gas',args,0)
    time.sleep(2)
    Obs_p1=read_obs(Nod_num,obs_Num,i)
    for ii in xrange(obs_num):
        y_obs_prediction[ii][i]=Obs_p1[ii]  #组成观测点处的预测值矩阵
    p1_predict=read_p(Nod_num,i)
    for jj in xrange(Nod_num):
        p_after[jj][i]=p1_predict[jj]     #组成状态变量预测值矩阵

taskpool=pool.Pool(4)
for i in xrange(N):
    taskpool.spawn(runexe,ki_initial,p1_initial,i)
    print i
taskpool.join()
print time.ctime()

x=np.vstack((para_initial,p_after))
np.savetxt('x.txt',x)
x_average=np.average(x,axis=1)
# np.savetxt('x_average.txt',x_average)
y_obs_pre_ava=np.average(y_obs_prediction,axis=1)
# np.savetxt('y_obs_pre_ave.txt',y_obs_pre_ava)
x_error=np.zeros([Nod_num*2,N])
y_error=np.zeros([obs_num,N])
for i in range(N):
    x_error[:,i]=x[:,i]-x_average[:]
    y_error[:,i]=y_obs_prediction[:,i]-y_obs_pre_ava[:]


np.savetxt('x_error.txt',x_error)
np.savetxt('y_error.txt',y_error)
np.savetxt('y_error_T.txt',y_error.T)
ph=np.dot(x_error,y_error.T)/(N-1)
np.savetxt('ph.txt',ph)
ph=np.matrix(ph)
hph=np.dot(y_error,y_error.T)/(N-1)
#np.savetxt('hph.txt',hph)
hph=np.matrix(hph+varR)
hph_var=np.linalg.pinv(hph)
#np.savetxt('hph_var.txt',hph_var)
k=np.dot(ph,hph_var)
k=np.array(k)
#np.savetxt('k.txt',k)
yy=np.zeros([obs_num,N])
for i in range(N):
    yy[:,i]=y_obs_p1[:,i]-y_obs_prediction[:,i]
    x[:,i]=x[:,i]+np.dot(k,(y_obs_p1[:,i]-y_obs_prediction[:,i]))

xx=x[0:Nod_num,:]    #需要大致检查x的每个元素，参数部分必须是负值，应该是ln(1e-18)左右的值，如果出现了正值，立马结束程序，另外状态变量出现了负值也立马结束程序
p1_1=x[Nod_num:Nod_num*2,:]
np.savetxt('t_1.txt',xx)
t_1_ave=xx.mean(axis=1)
np.savetxt('t_1_ave.txt',t_1_ave)
np.savetxt('yy.txt',yy)
# np.savetxt('x_1.txt',x)
if np.any(xx>0):
    print 'there is positive parameter'
    exit()
if np.any(p1_1<0):
    print 'there is negative p1'
    exit()

parY=np.zeros((Nod_num,time_step))
parY[:,0]=np.average(x[0:Nod_num,:],axis=1)
np.savetxt('parY_1.txt',parY[:,0])
df=pd.DataFrame(parY[:,0])
stat=df.describe()
std=stat.ix['std',[0]]
try:
    cov_init=np.sqrt(np.power(e,np.power(sigma,2))-1)
    cov=np.sqrt(np.power(e,np.power(std,2))-1)
    print 'initial covariance:',cov_init
    print 'std-1',std
    print 'cov_1',cov
except OverflowError:
    print 'cov is too large'
print time.ctime()


for t in range(2,time_step+1):
    try:
        KI=x[0:Nod_num,:]   #取出状态向量中的参数，将其进行指数恢复
        p1_update=x[Nod_num:Nod_num*2,:]
        KI=np.exp(KI)
        # for i in xrange(N):    #采用restart方法的时候需要修改时间
        #     time_modify(t,i)

        taskpool1=pool.Pool(4)
        for i in range(N):
            taskpool1.spawn(runexe,KI,p1_update,i)
            print i,'12'
        taskpool1.join()

        np.savetxt('p_after_%d.txt'%t,p_after)
        np.savetxt('y_obs_prediction_%d.txt'%t,y_obs_prediction)
        x=np.vstack((para_initial,p_after))
        x_average=np.average(x,axis=1)
        y_obs_pre_ava=np.average(y_obs_prediction,axis=1)
        x_error=np.zeros([Nod_num*2,N])
        y_error=np.zeros([obs_num,N])

        y_p1=obs_Pressure1[t]
        y_obs_p1=pd.DataFrame(y_p1)
        y_obs_p1=y_obs_p1.T
        y_obs_p1=y_obs_p1.values
        for i in range(N):
            x_error[:,i]=x[:,i]-x_average[:]
            y_error[:,i]=y_obs_prediction[:,i]-y_obs_pre_ava[:]

        ph=np.dot(x_error,y_error.T)/(N-1)
        ph=np.matrix(ph)
        np.savetxt('ph_%d.txt' %t,ph)
        hph=np.dot(y_error,y_error.T)/(N-1)
        hph=np.matrix(hph+varR)
        hph_var=np.linalg.pinv(hph)
        k=np.dot(ph,hph_var)
        k=np.array(k)
#        np.savetxt('k_%d.txt' %t,k)
        yy=np.zeros([obs_num,N])
        for i in range(N):
            yy[:,i]=y_obs_p1[:,i]-y_obs_prediction[:,i]
            x[:,i]=x[:,i]+np.dot(k,(y_obs_p1[:,i]-y_obs_prediction[:,i]))
        xx=x[0:Nod_num,:]
        p1_1=x[Nod_num:Nod_num*2,:]
        # if np.any(xx>0):
        #     exit()
        # if np.any(p1_1<0):
        #     exit()
        # if np.any(p1_2<0):
        #     exit()
        np.savetxt('t_%d.txt' %t,xx)
        t_n_ave=xx.mean(axis=1)
        np.savetxt('t_%d_ave.txt' %t,t_n_ave)
#        np.savetxt('x_%d.txt'%t,x)
#        np.savetxt('yy_%d.txt' %t,yy)
        parY[:,t-1]=np.average(x[0:Nod_num,:],axis=1)
        np.savetxt('parY.txt',parY)
        df=pd.DataFrame(parY[:,t-1])
        stat=df.describe()
        std=stat.ix['std',[0]]
        try:
            cov=math.sqrt(math.pow(e,math.pow(std,2))-1)
            print 't_%d_std:'%t,std
            print 't_%d_cov:'%t,cov
        except OverflowError:
            print 'cov is too large'
        pass
    except Exception,e:
        print e
    print time.ctime()



