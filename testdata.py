import os
import torch.backends.cudnn as cudnn
import opts
import train
import utils
import models.__init__ as init
import datasets.getdata as ld
import matplotlib
import matplotlib.pyplot as plt
import torchvision
from torchvision import transforms
import scipy.io as sio
import torch

parser = opts.myargparser()

global opt
opt = parser.parse_args()
dataloader = ld.GazeFollow(opt)
images, xis, eye_coords, pred_coords, eyes, names, eyes2, gaze2 = next(iter(dataloader.val_loader))

untr = transforms.Compose([
        transforms.Normalize([0, 0, 0], [1/(0.229), 1/(0.224), 1/(0.225)])])
untr2 = transforms.Compose([
        transforms.Normalize([-0.485, -0.456, -0.406], [1, 1, 1])])

for i in range(64):

    name = names[i]
    img = untr(images[i])
    img2 = untr(xis[i])

    img = untr2(img)
    img2 = untr2(img2)

    ey = eyes2[i]
    eye = eye_coords[i].view(1, 169)
    pred = pred_coords[i].view(1, 169)

    ind = pred.max(1)[1]
    step = 1 / 26.0
    y = ((float(ind[0]/ 13)) / 13.0) + step
    x = ((float(ind[0] % 13)) / 13.0) + step

    to_pil = torchvision.transforms.ToPILImage()
    im = to_pil(img)
    im2 = to_pil(img2)
    eye_np = eyes[i].cpu().numpy()
    eye_np2 = eyes2[i].cpu().numpy()
    print(name)
    print(eye_np)
    print(x * 227, y * 227)

    plt.subplot(131)
    plt.plot([x* 227, eye_np[0]* 227],[y* 227, eye_np[1]* 227])
    plt.imshow(im)
    plt.subplot(133)
    plt.plot([0, eye_np2[0]*227], [0, eye_np2[1]*227])
    plt.imshow(im2)
    plt.subplot(132)
    plt.imshow(eye_coords[i].cpu().numpy())
    plt.show()
