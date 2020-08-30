#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.nn.functional as F
import scipy.sparse as sp 
import numpy as np
from .model_base import Info, Model
from config import CONFIG


def graph_generating(raw_graph, row, col):
    if raw_graph.shape == (row, col):
        graph = sp.bmat([[sp.identity(raw_graph.shape[0]), raw_graph],
                             [raw_graph.T, sp.identity(raw_graph.shape[1])]])
    else:
        raise ValueError(r"raw_graph's shape is wrong")
    return graph

def laplace_transform(graph):
    rowsum_sqrt = sp.diags(1/(np.sqrt(graph.sum(axis=1).A.ravel()) + 1e-8))
    colsum_sqrt = sp.diags(1/(np.sqrt(graph.sum(axis=0).A.ravel()) + 1e-8))
    graph = rowsum_sqrt @ graph @ colsum_sqrt
    return graph

def to_tensor(graph):
    graph = graph.tocoo()
    values = graph.data
    indices = np.vstack((graph.row, graph.col))
    graph = torch.sparse.FloatTensor(torch.LongTensor(indices), torch.FloatTensor(values), 
                                          torch.Size(graph.shape))
    return graph

def print_graph_density(graph, name):
    print(name + ' density--------------------')
    print(len(graph.data)/(graph.shape[0]*graph.shape[1])) 


class BGCN_Info(Info):
    def __init__(self, embedding_size, embed_L2_norm, mess_dropout, node_dropout, num_layers, act=nn.LeakyReLU()):
        super().__init__(embedding_size, embed_L2_norm)
        self.act = act
        assert 1 > mess_dropout >= 0
        self.mess_dropout = mess_dropout
        assert 1 > node_dropout >= 0
        self.node_dropout = node_dropout
        assert isinstance(num_layers, int) and num_layers > 0
        self.num_layers = num_layers


class BGCN(Model):
    def get_infotype(self):
        return BGCN_Info

    def __init__(self, info, dataset, raw_graph, device, pretrain=None):
        super().__init__(info, dataset, create_embeddings=True)
        self.items_feature = nn.Parameter(
            torch.FloatTensor(self.num_items, self.embedding_size))
        nn.init.xavier_normal_(self.items_feature)

        self.epison = 1e-8

        assert isinstance(raw_graph, list)
        ub_graph, ui_graph, bi_graph = raw_graph
        bb_graph = bi_graph @ bi_graph.T

        #  deal with weights
        bundle_size = bi_graph.sum(axis=1) + 1e-8
        bb_graph @= sp.diags(1/bundle_size.A.ravel())

        #  pooling graph
        bi_graph @= sp.diags(1/bundle_size.A.ravel())

        print_graph_density(bb_graph, 'bb graph')
        print_graph_density(ub_graph, 'ub graph')

        if ui_graph.shape == (self.num_users, self.num_items):
            # 自环路（Self-Loop）对邻接节点和节点本身分别训练一组权重参数
            atom_graph = sp.bmat([[sp.identity(ui_graph.shape[0]), ui_graph],
                                 [ui_graph.T, sp.identity(ui_graph.shape[1])]])
        else:
            raise ValueError(r"raw_graph's shape is wrong")
        self.atom_graph = to_tensor(laplace_transform(atom_graph)).to(device)
        print('finish generating atom graph')
 
        if ub_graph.shape == (self.num_users, self.num_bundles) \
                and bb_graph.shape == (self.num_bundles, self.num_bundles):
            # 自环路（Self-Loop）对邻接节点和节点本身分别训练一组权重参数
            non_atom_graph = sp.bmat([[sp.identity(ub_graph.shape[0]), ub_graph],
                                 [ub_graph.T, bb_graph]])
        else:
            raise ValueError(r"raw_graph's shape is wrong")
        self.non_atom_graph = to_tensor(laplace_transform(non_atom_graph)).to(device)
        print('finish generating non-atom graph')

        self.pooling_graph = to_tensor(bi_graph).to(device)
        print('finish generating pooling graph')

        # copy from info
        self.act = self.info.act
        self.num_layers = self.info.num_layers
        self.device = device

        #  Dropouts
        self.mess_dropout = nn.Dropout(self.info.mess_dropout, True)
        self.node_dropout = nn.Dropout(self.info.node_dropout, True)

        # Layers
        self.dnns_atom = nn.ModuleList([nn.Linear(
            self.embedding_size, self.embedding_size) for _ in range(self.num_layers)])
        self.dnns_non_atom = nn.ModuleList([nn.Linear(
            self.embedding_size, self.embedding_size) for _ in range(self.num_layers)])

        # pretrain
        if not pretrain is None:
            self.users_feature.data = F.normalize(
                pretrain['users_feature'])  
            self.items_feature.data = F.normalize(
                pretrain['items_feature'])
            self.bundles_feature.data = F.normalize(
                pretrain['bundles_feature'])


