# -*- coding: utf-8 -*-
import h5py
from h5py import Dataset, Group, File
import numpy as np
import sys
from keras.models import Sequential, load_model

sys.setrecursionlimit(10000) # 100000  Segmentation fault (core dumped)

def recursive_ascii_encode(lst):
    ret = []
    for x in lst:
        if isinstance(x, Group):  # covers both str and unicode
            ret.append(x.encode('ascii', 'ignore'))
        else:
            ret.append(recursive_ascii_encode(x))
            
    return ret

# rnnSyscallNum = np.load("/home/hz/ws/share/gitlabshare/pyData-master/pyData/ins_log_syscallnum.h5")
# print("rnnSyscallNum: %s" % str(rnnSyscallNum))
rnnSyscallNumPath = "/home/hz/ws/share/gitlabshare/pyData-master/pyData/ins_log_syscallnum.h5"
with h5py.File(rnnSyscallNumPath,'r') as f:
    for fkey in f.keys():
        print("f[fkey]: %s  \tfkey: %s  \tf[fkey].name: %s" % (f[fkey], fkey, f[fkey].name))
        print("type(fkey): %s" % type(fkey))

    # a = f[str(fkey)][:]
    # print("a: %s " % recursive_ascii_encode(f))
    print("--")


# f[fkey]: <HDF5 group "/model_weights" (3 members)>  	fkey: model_weights  	f[fkey].name: /model_weights
# f[fkey]: <HDF5 group "/optimizer_weights" (2 members)>  	fkey: optimizer_weights  	f[fkey].name: /optimizer_weights

model = load_model(rnnSyscallNumPath)
for layer in model.layers:
    weights = layer.get_weights() # list of numpy arrays
    print("weights : %s" % str(weights))

