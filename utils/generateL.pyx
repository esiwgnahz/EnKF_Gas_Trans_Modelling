#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zq'

import numpy as np
import math
cimport numpy
cdef extern from "math.h":
    float pow(float sigma,float num)
    float exp(float dishu)
    float fabs(float xx)
def generateL(double sigma,double lax,double lay,double dx,double dy,int m,int n):
    cdef int mn=m*n
    cdef numpy.ndarray c=np.zeros((mn,mn))
    cdef int i
    cdef int j
    cdef int xi,xj
    cdef double yi,yj
    for i in xrange(mn):
        for j in xrange(mn):
            xi=int(math.floor(i/m))+1
            yi=i-m*(xi-1)
            xj=int(math.floor(j/m))+1
            yj=j-m*(xj-1)
            if yi==0:
                xi=int(math.floor(i/m))
                yi=m
            if yj==0:
                xj=int(math.floor(j/m))
                yj=m
            c[i,j]=pow(sigma,2)*(exp(-fabs((xi-xj)*dx)/lax-fabs((yi-yj)*dy)/lay))

    L=np.linalg.cholesky(c)
    return L