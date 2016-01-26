#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'

def remove_generate_files(N):
    import os
    import shutil
    for i in xrange(N):
        file_args=r'E:\EnKF_Gas_Modelling\gas_{0}'.format(i)
        old=r'E:\EnKF_Gas_Modelling\gas_00'
        if os.path.exists(file_args):
            shutil.rmtree(file_args)
            shutil.copytree(old,file_args)
        else:
            shutil.copytree(old,file_args)

if __name__=='__main__':
    remove_generate_files(100)