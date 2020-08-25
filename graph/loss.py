import os
import torch
import numpy as np
import scipy.sparse as sp 
from torch.utils.data import Dataset
from config import CONFIG

class _Loss(nn.Moudle):
    def __init__(self,reduction='sum')
        super().__init__()
        assert(reduction == 'mean' or reduction == 'sum' or reduction == 'none')
        self.reduction = reduction

class BPRloss(_Loss):
    """docstring for BPRloss"""
    def __init__(self, reduction='sum'):
        super().__init__(reduction)

    def forward(self, model_output, **kwargs):
        pred, L2_loss = model_output
        # BPR loss
        loss = -torch.log(torch.sigmoid(pred[:, 0] - pred[:, 1]))
        # reduction
        if self.reduction == 'mean':
            loss = torch.mean(loss)
        elif self.reduction == 'sum':
            loss = torch.sum(loss)
        elif self.reduction == 'none':
            pass
        else:
            raise ValueError("reduction must be  'none' | 'mean' | 'sum'")
        loss += L2_loss / kwargs['batch_size'] if 'batch_size' in kwargs else 0
        return loss       