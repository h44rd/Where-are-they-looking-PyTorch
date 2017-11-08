import torch
import torch.nn as nn
from torch.nn import init
import copy
import random
import math
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt

class AverageMeter():
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

def visualize_gaze(images, eye_coords, pred_coords):

    img = images[0]
    eye = eye_coords[0].view(1, 169)
    pred = pred_coords[0].view(1, 225)

    ind = pred.max(1)[1]
    step = 1 / 30.0
    x = ((float(ind/ 15)) / 15.0) + step
    y = ((float(ind % 15)) / 15.0) + step

    e = eye.max(1)[1]
    ex = ((float(e/ 13)) / 15.0) + step
    ey = ((float(e % 13)) / 15.0) + step

    plt.imshow(img)
    plt.show()
    print(x, y, ex, ey)

def AUCaccuracy(output, target, opt):
    pass

def adjust_learning_rate(opt, optimizer, epoch):
    epoch = copy.deepcopy(epoch)
    lr = opt.maxlr
    wd = opt.weightDecay
    if opt.learningratescheduler == 'decayschedular':
        while epoch >= opt.decayinterval:
            lr = lr/opt.decaylevel
            epoch = epoch - opt.decayinterval
    lr = max(lr, opt.minlr)
    opt.lr = lr

    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
        param_group['weight_decay'] = wd

def get_mean_and_std(dataloader):
    '''Compute the mean and std value of dataset.'''
    mean = torch.zeros(3)
    std = torch.zeros(3)
    len_dataset = 0
    print('==> Computing mean and std..')
    for inputs, targets in dataloader:
        len_dataset += 1
        for i in range(len(inputs[0])):
            mean[i] += inputs[:,i,:,:].mean()
            std[i] += inputs[:,i,:,:].std()
    mean.div_(len_dataset)
    std.div_(len_dataset)
    return mean, std

def weights_init(model, opt):
    '''Perform weight initializations.'''
    for m in model.modules():
        if isinstance(m, nn.Conv2d):
            c  = math.sqrt(2.0 / (m.kernel_size[0] * m.kernel_size[1] * m.out_channels))
            m.weight.data = torch.randn(m.weight.data.size()).cuda() * c #*0.1
            if m.bias is not None:
                init.constant(m.bias, 0)
        elif isinstance(m, nn.BatchNorm2d):
            if m.affine == True:
                init.constant(m.weight, 1)
                init.constant(m.bias, 0)
        elif isinstance(m, nn.Linear):
            c =  math.sqrt(2.0 / m.weight.data.size(1));
            if m.bias is not None:
                init.constant(m.bias, 0)
