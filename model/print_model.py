# -*- coding: utf-8 -*-
import h5py
import numpy as np

vocab = np.load("vocab")
print("vocab: %s" % str(vocab))

embeddings = np.load("embeddings.npy")
print("embeddings.npy: %s" % str(embeddings))

model = np.load("model")
print("model: %s" % str(model))
