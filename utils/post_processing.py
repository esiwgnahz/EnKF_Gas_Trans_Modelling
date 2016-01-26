#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'

import numpy as np
import math
import matplotlib.pyplot as plt
class post_calculation:
    '''
    t is the current time-step
    time_step is the total timesteps
    Nod_num is the number of nodes
    '''
    def __init__(self,t,time_step,Nod_num):
        self.t=t
        self.time_step=time_step
        self.Nod_num=Nod_num

    def spread_calculation(self):
        a=np.zeros((self.t))
        for i in range(1,self.t+1):
            args=r'E:\EnKF_Gas_Modelling\t_%d.txt' % i
            f=open(args,'r')
            content=f.readlines()
            for line in range(len(content)):
                content[line]=content[line].split()
                pass
            content=np.array(content)
            content=np.float64(content)
            var=np.var(content,axis=1)
            std=np.sqrt(np.mean(var,axis=0))
            a[i-1]=std
            pass
        x=[x+1 for x in range(self.t)]
        print a
        plt.plot(x,a,'r')
        plt.title('spread')
        plt.show()


    def rmse_calculation(self):
        para_args=r'E:\EnKF_Gas_Modelling\true_obs\para_true.txt'
        with open(para_args,'r') as f:
            content=f.readlines()
        for i in range(len(content)):
            content[i]=content[i].split()

        content=np.array(content)
        content=np.float64(content)
        content=content[:,0]
        content=np.array(content)
        para_true=content
  
        parY_args=r'E:\EnKF_Gas_Modelling\parY.txt'
        with open(parY_args,'r') as f:
            content_parY=f.readlines()
        for i in range(len(content_parY)):
            content_parY[i]=content_parY[i].split()
        content_parY=np.array(content_parY)
        content_parY=np.float64(content_parY)
        parY=content_parY

        rmse=np.zeros((self.time_step,1))
        for i in range(self.t):
            par_Y=parY[:,i]
#            print par_Y.shape
            rmse[i,0]=math.sqrt(sum((par_Y-para_true)**2))/(self.Nod_num-1)
        X=[i+1 for i in range(self.time_step)]
        Y=rmse
        plt.plot(X,Y,'r')
        plt.title('rmse')
        plt.show()
        return rmse

if __name__=='__main__':
    a=post_calculation(5,20,1681)
    a.spread_calculation()
    print a.rmse_calculation()
