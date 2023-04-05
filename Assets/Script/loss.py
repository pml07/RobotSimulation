import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt


DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
def total_loss(y, output):
    # print('y: ', y)
    # print('real output: ',output) # grad
    r1 = ((output[:, 0] + 1) / 2) * (165 - (-165)) + (-165)
    r2 = ((output[:, 1] + 1) / 2) * (85 - (-125)) + (-125) 
    r3 = ((output[:, 2] + 1) / 2) * (185 - (-55)) + (-55)
    r4 = ((output[:, 3] + 1) / 2) * (190 - (-190)) + (-190)
    r5 = ((output[:, 4] + 1) / 2) * (115 - (-115)) + (-115)
    r6 = ((output[:, 5] + 1) / 2) * (5 - (-5)) + (-5)
    
    # output = "r1 = {}, r2 = {}, r3 = {}, r4 = {}, r5 = {}, r6 = {}".format(r1.item(), r2.item(), r3.item(), r4.item(), r5.item(), r6.item())
    # with open("output/output.txt" , "a") as f:
    #     f.write(output)
    #     f.write("\n")
    
    loss = torch.abs(y[:, 0] - r1) + torch.abs(y[:, 1] - r2) + torch.abs(y[:, 2] - r3) + torch.abs(y[:, 3] - r4) + torch.abs(y[:, 4] - r5) + torch.abs(y[:, 5] - r6)
    # print(loss)
    return loss
    
    
