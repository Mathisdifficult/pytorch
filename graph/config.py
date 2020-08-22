#!/usr/bin/env python3
# -*- coding: utf-8 -*-

CONFIG = {

    'model': 'BGCN',
    'dataset_name': 'NetEase',
    'task': 'tune',
    'eval_task': 'test',

    'lrs': [3e-4],
    'message_dropouts': [0],
    'node_dropouts': [0], 
    'decays': [1e-7],


}

