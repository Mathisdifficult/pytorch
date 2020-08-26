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
#继承Dataset
class BasicDataset(Dataset):
    def __init__(self, path, name, task, neg_sample):
        self.path = path
        self.name = name
        self.task = task
        self.neg_sample = neg_sample
        self.num_users, self.num_bundles, self.num_items  = self.__load_data_size()
#覆写torch.utils.data.Dataset其中的两个方法,覆写这两个方法会直接返回错误。
    def __getitem__(self, index):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError
    #对data文件夹中，某一txt文件数据按照（\t）行呈list返回数据  
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

class BundleTrainDataset(BasicDataset):
    def __init__(self, path, name, item_data, assist_data, seed=None):
        super().__init__(path,name,'train',1)
        #User-Bundle
        self.U_B_pairs = self.load_U_B_interaction()
        indice = np.array(self.U_B_pairs, dtype=np.int32)
        values = np.ones(len(self.U_B_pairs), dtype=np.float32)
        self.ground_truth_u_b = sp.coo_matrix(
            (values, (indice[:, 0], indice[:, 1])), shape=(self.num_users, self.num_bundles)).tocsr()
#获取某个index下标的user_b, pos_bundle    
    def __getitem__(self, index):
        user_b, pos_bundle = self.U_B_pairs[index]
        all_bundles = [pos_bundle]
        while True:
            i = np.random.randint(self.num_bundles)
            if self.ground_truth_u_b[user_b, i] == 0 and not i in all_bundles:
                all_bundles.append(i)
                if len(all_bundles) == self.neg_sample+1:
                    break

class BundleTestDataset(BasicDataset):
    def __init__(self, path, name, train_dataset, task='test'):
        super().__init__(path, name, task, None)
        #User-Bundle
        self.U_B_pairs = self.load_U_B_interaction()
        indice = np.array(self.U_B_pairs, dtype=np.int32)
        values = np.ones(len(self.U_B_pairs), dtype=np.float32)
        self.ground_truth_u_b = sp.coo_matrix(
            (values, (indice[:, 0], indice[:, 1])), shape=(self.num_users, self.num_bundles)).tocsr()

    def __getitem__(self, index):
        return index, torch.from_numpy(self.ground_truth_u_b[index].toarray()).squeeze(),  \
            torch.from_numpy(self.train_mask_u_b[index].toarray()).squeeze(),  \

    def __len__(self):
        return self.ground_truth_u_b.shape[0]

class ItemDataset(BasicDataset):
    def __init__(self, path, name, assist_data, seed=None):
        super().__init__(path, name, 'train', 1)
        # User-Item
        self.U_I_pairs = self.load_U_I_interaction()
        indice = np.array(self.U_I_pairs, dtype=np.int32)
        values = np.ones(len(self.U_I_pairs), dtype=np.float32)
        self.ground_truth_u_i = sp.coo_matrix( 
            (values, (indice[:, 0], indice[:, 1])), shape=(self.num_users, self.num_items)).tocsr()
    def __getitem__(self, index):
        user_i, pos_item = self.U_I_pairs[index]
        all_items = [pos_item]
        while True:
            j = np.random.randint(self.num_items)
            if self.ground_truth_u_i[user_i, j] == 0 and not j in all_items:
                all_items.append(j)
                if len(all_items) == self.neg_sample+1:
                    break

        return torch.LongTensor([user_i]), torch.LongTensor(all_items)









        



