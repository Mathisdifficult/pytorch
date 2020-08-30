#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from torch.utils.data import DataLoader
import setproctitle
import dataset
from model import BGCN, BGCN_Info
from utils import check_overfitting, early_stop, logger
from train import train
from metric import Recall, NDCG, MRR
from config import CONFIG
from test import test
import loss
from itertools import product
import time
#  from utils.visshow import VisShow
from tensorboardX import SummaryWriter

def main():
    device = torch.device('cpu')

    seed = 123
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

    #  load data
    bundle_train_data, bundle_test_data, item_data, assist_data = \
            dataset.get_dataset(CONFIG['path'], CONFIG['dataset_name'], task=CONFIG['task'])

    train_loader = DataLoader(bundle_train_data, 2048, True,
                              num_workers=8, pin_memory=True)
    test_loader = DataLoader(bundle_test_data, 4096, False,
                             num_workers=16, pin_memory=True)

    #  graph
    ub_graph = bundle_train_data.ground_truth_u_b
    ui_graph = item_data.ground_truth_u_i
    bi_graph = assist_data.ground_truth_b_i

    #  metric
    metrics = [Recall(20), NDCG(20), Recall(40), NDCG(40), Recall(80), NDCG(80)]
    TARGET = 'Recall@20'

    #  loss
    loss_func = loss.BPRLoss('mean')

    #  log
    log = logger.Logger(os.path.join(
        CONFIG['log'], CONFIG['dataset_name'], 
        f"{CONFIG['model']}_{CONFIG['task']}", ''), 'best', checkpoint_target=TARGET)

    time_path = time.strftime("%y%m%d-%H%M%S", time.localtime(time.time()))

    for lr, decay, message_dropout, node_dropout \
            in product(CONFIG['lrs'], CONFIG['decays'], CONFIG['message_dropouts'], CONFIG['node_dropouts']):
        # vis = VisShow('localhost', 16666,
        #               f'{CONFIG['dataset_name']}-{MODELTYPE.__name__}-{decay}-{lr}-{theta}-3layer')

        visual_path =  os.path.join(CONFIG['visual'], 
                                    CONFIG['dataset_name'],  
                                    f"{CONFIG['model']}_{CONFIG['task']}", 
                                    f"{time_path}@{CONFIG['note']}", 
                                    f"lr{lr}_decay{decay}_medr{message_dropout}_nodr{node_dropout}")
        
        # model
        graph = [ub_graph, ui_graph, bi_graph]
        info = BGCN_Info(64, decay, message_dropout, node_dropout, 1)
        model = BGCN(info, assist_data, graph, device, pretrain=None).to(device)

        # op
        op = optim.Adam(model.parameters(), lr=lr)
        # env
        env = {'lr': lr,
               'op': str(op).split(' ')[0],   # Adam
               'dataset': CONFIG['dataset_name'],
               'model': CONFIG['model'], 
               'sample': CONFIG['sample'],
               }



if __name__ == "__main__":
    main()
