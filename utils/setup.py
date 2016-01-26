# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

ext_modules=[Extension("generateL",["generateL.pyx"],include_dirs=[numpy.get_include()])]
setup(name='GenerateL app',cmdclass={'build_ext':build_ext},ext_modules=ext_modules)

# import math
# import numpy as np
# sigma=0.6
# deltax=1
# deltay=0.5
# dx=0.02
# dy=0.02
# x=2
# y=1
# m=int(y/dy+1)
# n=int(x/dx+1)
# # generateL(sigma,deltax,deltay,dx,dy,m,n)
# mn=m*n
# def c(i,j,mn,lax,lay):
#     c=np.zeros((mn,mn))
#     xi=int(math.floor(i/m))+1
#     yi=i-m*(xi-1)
#     xj=int(math.floor(j/m))+1
#     yj=j-m*(xj-1)
#     if yi==0:
#         xi=int(math.floor(i/m))
#         yi=m
#     if yj==0:
#         xj=int(math.floor(j/m))
#         yj=m
#     c[i,j]=math.pow(sigma,2)*(math.exp(-math.fabs((xi-xj)*dx)/lax-math.fabs((yi-yj)*dy)/lay))
#
# generate=np.frompyfunc(c,5,1)
# k=np.arange(mn)
# p=np.arange(mn)
# y=generate(k,p,mn,deltax,deltay)
# y=y.astype(np.float)
