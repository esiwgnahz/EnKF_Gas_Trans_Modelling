#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'


def time_modify(t,i):
    args_tim=r'E:\EnKF_Gas_Modelling\gas_{0}\gas.tim'.format(i)
    with open(args_tim,'r') as f:
        content=f.readlines()
        line_modify_1=content[5]
        line_modify_2=content[9]
        line_modify_3=content[16]
        line_modify_4=content[20]
        modify_1=line_modify_1.split()
        modify_1[0]='{0}'.format(t)
        line_modify_1=' '.join(modify_1[i] for i in range(len(modify_1)))+'\n'
        modify_2=line_modify_2.split()
        modify_2[0]='{0}'.format(t*50)
        line_modify_2=' '.join(modify_2[i] for i in range(len(modify_2)))+'\n'
        modify_3=line_modify_3.split()
        modify_3[0]='{0}'.format(t)
        line_modify_3=' '.join(modify_3[i] for i in range(len(modify_3)))+'\n'
        modify_4=line_modify_4.split()
        modify_4[0]='{0}'.format(t*50)
        line_modify_4=' '.join(modify_4[i] for i in range(len(modify_4)))+'\n'
        content[5]=line_modify_1
        content[9]=line_modify_2
        content[16]=line_modify_3
        content[20]=line_modify_4
    with open(args_tim,'w') as f:
        for line in content:
            f.write(line)

if __name__=='__main__':
    time_modify(3,87)

