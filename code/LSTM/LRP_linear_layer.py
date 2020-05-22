'''
@author: Leila Arras
@maintainer: Leila Arras
@date: 21.06.2017
@version: 1.0+
@copyright: Copyright (c) 2017, Leila Arras, Gregoire Montavon, Klaus-Robert Mueller, Wojciech Samek
@license: see LICENSE file in repository root
'''
# -*- coding: utf-8 -*-

import numpy as np
from numpy import newaxis as na
import inspect, re

# is_log = True

def printvar(var, is_log = False, namespace=globals()):
# def printvar(var, is_log = False):
    if is_log:
        varname = [name for name in namespace if namespace[name] is var]
        # varname = [ k for k,v in locals().items() if v == var][0] #Python3.x中不再支持iteritems()，所以将iteritems()改成items().
        varname = "default_varname"
        varshape = str(np.shape(var))

        print("hz- varname:%s varshape:%s  varvalue:%s" % (varname, varshape, var))


def lrp_linear(hin, w, b, hout, Rout, bias_nb_units, eps, bias_factor=0.0, debug=False):
    """
    LRP for a linear layer with input dim D and output dim M.
    Args:
    - hin:            forward pass input, of shape (D,)   D=60
    - w:              connection weights, of shape (D, M) M=5
    - b:              biases, of shape (M,)
    - hout:           forward pass output, of shape (M,)    (unequal to   np.dot(w.T,hin)+b   if more than one incoming layer!)
    - Rout:           relevance at layer output, of shape (M,)
    - bias_nb_units:  total number of connected lower-layer units (onto which the bias/stabilizer contribution is redistributed for sanity check)
                        连接的下层单元总数（偏差/稳定器贡献重新分配到其单元上 以进行健全性检查）
    - eps:            stabilizer (small positive number)
    - bias_factor:    set to 1.0 to check global relevance conservation守恒, otherwise use 0.0 to ignore bias/stabilizer redistribution (recommended)
    Returns:
    - Rin:            relevance at layer input, of shape (D,)
    """
    sign_out = np.where(hout[na,:]>=0, 1., -1.) # shape (1, M)
    printvar(sign_out)
    
    numer    = (w * hin[:,na]) + ( bias_factor * (b[na,:]*1. + eps*sign_out*1.) / bias_nb_units ) # shape (D, M)..bias_nb_units=N
    # Note: here we multiply the bias_factor with both the bias b and the stabilizer eps since in fact
    # using the term "(b[na,:]*1. + eps*sign_out*1.) / bias_nb_units" in the 分子numerator is only useful for sanity check
    # (in the initial paper version we were using (bias_factor*b[na,:]*1. + eps*sign_out*1.) / bias_nb_units instead)
    
    # printvar(numer)#60*5
    
    denom    = hout[na,:] + (eps*sign_out*1.)   # shape (1, M)
    printvar(denom)#(1, 5)
    
    message  = (numer/denom) * Rout[na,:]       # shape (D, M)...numer/denom = R (i <- j)
    # printvar(message)#(60,5)
    
    Rin      = message.sum(axis=1)              # shape (D,)=(60,)
    # printvar(Rin)
    printvar(Rout)#varshape:(5,)  varvalue:[ 2.73149687  0.    0.     -0.      -0.]
    
    if debug:
        print("local diff: Rout.sum() - Rin.sum(): ", Rout.sum() - Rin.sum())#1.6742738366338374..
    # Note: 
    # - local  layer   relevance conservation守恒 if bias_factor==1.0 and bias_nb_units==D (i.e. when only one incoming layer)
    # - global network relevance conservation守恒 if bias_factor==1.0 and bias_nb_units set accordingly to the total number of lower-layer connections 
    # -> can be used for sanity check
    
    return Rin
