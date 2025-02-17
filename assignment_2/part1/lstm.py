################################################################################
# MIT License
#
# Copyright (c) 2019
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to conditions.
#
# Author: Deep Learning Course | Fall 2019
# Date Created: 2019-09-06
################################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch
import torch.nn as nn

################################################################################

class LSTM(nn.Module):

    def __init__(self, seq_length, input_dim, num_hidden, num_classes, device='cpu'):
        super(LSTM, self).__init__()
        self.wgh = nn.Parameter(torch.zeros((num_hidden, num_hidden), dtype=torch.double))
        self.wgx = nn.Parameter(torch.zeros((input_dim, num_hidden), dtype=torch.double))
        self.bg = nn.Parameter(torch.zeros((num_hidden), dtype=torch.double))
        
        self.wih = nn.Parameter(torch.zeros((num_hidden, num_hidden), dtype=torch.double))
        self.wix = nn.Parameter(torch.zeros((input_dim, num_hidden), dtype=torch.double))
        self.bi = nn.Parameter(torch.zeros((num_hidden), dtype=torch.double))

        self.wfh = nn.Parameter(torch.zeros((num_hidden, num_hidden), dtype=torch.double))
        self.wfx = nn.Parameter(torch.zeros((input_dim, num_hidden), dtype=torch.double))
        self.bf = nn.Parameter(torch.ones((num_hidden), dtype=torch.double))

        self.woh = nn.Parameter(torch.zeros((num_hidden, num_hidden), dtype=torch.double))
        self.wox = nn.Parameter(torch.zeros((input_dim, num_hidden), dtype=torch.double))
        self.bo = nn.Parameter(torch.zeros((num_hidden), dtype=torch.double))

        self.wph = nn.Parameter(torch.zeros((num_hidden, num_classes), dtype=torch.double))
        self.bp = nn.Parameter(torch.zeros((num_classes), dtype=torch.double))

        self.sequence_length = seq_length

        self.h = torch.zeros((num_hidden), dtype=torch.double).to(device)
        self.c = torch.zeros((num_hidden), dtype=torch.double).to(device)
        self.h_list = []
        

        torch.nn.init.kaiming_uniform_(self.wgh)
        torch.nn.init.kaiming_uniform_(self.wgx)

        torch.nn.init.kaiming_uniform_(self.wih)
        torch.nn.init.kaiming_uniform_(self.wix)
        
        torch.nn.init.kaiming_uniform_(self.wfh)
        torch.nn.init.kaiming_uniform_(self.wfx)

        torch.nn.init.kaiming_uniform_(self.woh)
        torch.nn.init.kaiming_uniform_(self.wox)

        torch.nn.init.kaiming_uniform_(self.wph)
        

    def forward(self, x):
        # Implementation here ...
        # h, and save grad

        h_prev = self.h
        c_prev = self.c
        self.h_list = []
        for t in range(self.sequence_length):
            gt = (x[:, t] @ self.wgx + h_prev @ self.wgh + self.bg).tanh()
            it = (x[:, t] @ self.wix + h_prev @ self.wih + self.bi).sigmoid()
            ft = (x[:, t] @ self.wfx + h_prev @ self.wfh + self.bf).sigmoid()
            ot = (x[:, t] @ self.wox + h_prev @ self.woh + self.bo).sigmoid()
            ct = gt * it + c_prev * ft
            ht = (ct).tanh() * ot
            ht.retain_grad()
            self.h_list.append(ht)
            c_prev = ct
            h_prev = ht
            
        p = ht @ self.wph  + self.bp
        return p
