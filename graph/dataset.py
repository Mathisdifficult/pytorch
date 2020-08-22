#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import torch
import numpy as np
import scipy.sparse as sp 
from torch.utils.data import Dataset
from config import CONFIG

def sparse_ones(indices, size, dtype=torch.float):
    one = torch.ones(indices.shape[1], dtype=dtype)
    return torch.sparse.FloatTensor(indices, one, size=size).to(dtype)

def to_tensor(graph):
    graph = graph.tocoo()
    values = graph.data
    indices = np.vstack((graph.row, graph.col))
    graph = torch.sparse.FloatTensor(torch.LongTensor(indices), torch.FloatTensor(values), 
                                          torch.Size(graph.shape))
    return graph

class BasicDataset(Dataset):
    def __init__(self, path, name, task, neg_sample):
        self.path = path
        self.name = name
        self.task = task
        self.neg_sample = neg_sample
        self.num_users, self.num_bundles, self.num_items  = self.__load_data_size()

    def __getitem__(self, index):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError
        
    def __load_data_size(self):
        with open(os.path.join(self.path, self.name, '{}_data_size.txt'.format(self.name)), 'r') as f:
            return [int(s) for s in f.readline().split('\t')][:3]
    def load_U_B_interaction(self):
        with open(os.path.join(self.path, self.name, 'user_bundle_{}.txt'.format(self.task)), 'r') as f:
            return list(map(lambda s: tuple(int(i) for i in s[:-1].split('\t')), f.readlines()))
    def load_U_I_interaction(self):
        with open(os.path.join(self.path, self.name, 'user_item.txt'), 'r') as f:
            return list(map(lambda s: tuple(int(i) for i in s[:-1].split('\t')), f.readlines()))
    def load_B_I_interaction(self):
        with open(os.path.join(self.path, self.name, 'bundle_item.txt'), 'r') as f:
            return list(map(lambda s: tuple(int(i) for i in s[:-1].split('\t')), f.readlines()))

