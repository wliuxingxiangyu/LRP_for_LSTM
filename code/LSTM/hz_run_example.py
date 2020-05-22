# -*- coding: utf-8 -*-

import sys
import codecs
import numpy as np
from IPython.display import display, HTML

#No module named 'code.LSTM'; 'code' is not a package..so todo fix LSTM_bidi.py
import LSTM_bidi.py
sys.append("../code/util/heatmap.py")
import heatmap.py

def get_test_sentence(sent_idx):
    """Returns an SST test set sentence and its true label, sent_idx must be an integer in [1, 2210]"""
    idx = 1
    with codecs.open("./data/sequence_test.txt", 'r', encoding='utf8') as f:
        for line in f:
            line          = line.rstrip('\n')
            line          = line.split('\t')
            true_class    = int(line[0])-1         # true class
            words         = line[1].split(' | ')   # sentence as list of words
            if idx == sent_idx:#返回 sent_idx 个数的word
                return words, true_class
            idx +=1

def predict(words):
    """Returns the classifier's predicted class"""
    net                 = LSTM_bidi()                                   # load trained LSTM model..from LSTM_bidi.py
    w_indices           = [net.voc.index(w) for w in words] # convert input sentence to word IDs..hz用系统调用号.
    printvar(w_indices, True)
    net.set_input(w_indices) # set LSTM input sequence..from LSTM_bidi.py
    scores              = net.forward()                                 # classification prediction scores
    print("hz- len(scores):%s scores: %s" % (len(scores), scores))
    printvar(net.get_para(), True)
    return np.argmax(scores)  #argmax() return max value index.# 五类情感，选可能性最大的分类 

words, _ = get_test_sentence(291)                                       # SST test set sentence number 291
printvar(words, True)

predicted_class = predict(words) # get predicted class..from run_example.ipynb
target_class    = predicted_class

print (words)
print ("\npredicted class: ",   predicted_class)

# LRP hyperparameters:
eps                 = 0.001                                             # small positive number
bias_factor         = 0.0                                               # recommended value
 
net                 = LSTM_bidi()                                       # load trained LSTM model

w_indices           = [net.voc.index(w) for w in words]                 # convert input sentence to word IDs
Rx, Rx_rev, R_rest  = net.lrp(w_indices, target_class, eps, bias_factor)# perform LRP
R_words             = np.sum(Rx + Rx_rev, axis=1)  #R表示相关性 compute word-level LRP relevances
scores              = net.s.copy()  


print ("prediction scores:        ",   scores)
print ("\nLRP target class:         ", target_class)
print ("\nLRP relevances:")
for idx, w in enumerate(words):
    print ("\t\t\t" + "{:8.2f}".format(R_words[idx]) + "\t" + w)
print ("\nLRP heatmap below:")    
display(HTML(html_heatmap(words, R_words)))#from IPython.display import display, HTML
# html_heatmap() from heatmap.py

# How to sanity check global relevance conservation:
bias_factor        = 1.0                                             # value to use for sanity check
Rx, Rx_rev, R_rest = net.lrp(w_indices, target_class, eps, bias_factor)
R_tot              = Rx.sum() + Rx_rev.sum() + R_rest.sum()#total:全部的 # sum of all "input" relevances

printvar(Rx,False)
printvar(Rx_rev, False)
printvar(R_rest, False)
print(R_tot)
print("Sanity check passed? ", np.allclose(R_tot, net.s[target_class]))
#np.allclos():比较两个array是不是每一元素都相等，默认在1e-05的误差范围内