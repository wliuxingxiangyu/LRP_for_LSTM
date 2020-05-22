# -*- coding: utf-8 -*-
import h5py
import numpy as np

vocab = np.load("vocab")
shape = np.shape(vocab)
print("vocab: shape%s \n %s" % (str(shape), str(vocab)))

embeddings = np.load("embeddings.npy")
shape = np.shape(embeddings)
print("embeddings.npy: shape%s \n %s" % (str(shape), str(embeddings)))

model = np.load("model")
shape = np.shape(model)
print("model: shape%s \n %s" % (str(shape),  str(model)))
