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

def calculate_distance(x, output):   
    x1 = x[0][-1][0:3]
    x2 = x[0][-1][3:6]
    x3 = x[0][-1][6:9]
    x4 = x[0][-1][9:12]
    x5 = x[0][-1][12:15]
    x6 = x[0][-1][15:18]
    # print('---------x6: ',x6)
    
    p1 = torch.tensor([0.0, 0.0, 0.0]).to(DEVICE)
    p2 = torch.tensor([0.0, 0.4, 0.0]).to(DEVICE)
    p3 = torch.tensor([0.0, 0.8, 0.0]).to(DEVICE)
    p4 = torch.tensor([0.0, 0.8, -0.3]).to(DEVICE)
    p5 = torch.tensor([0.0, 0.8, -0.5]).to(DEVICE)
    p6 = torch.tensor([0.0, 0.8, -0.6]).to(DEVICE)
    
    r1 = ((output[:, 0] + 1) / 2) * (165 - (-165)) + (-165)  # y
    r1 = torch.deg2rad(r1)
    r2 = ((output[:, 1] + 1) / 2) * (85 - (-125)) + (-125)  # x
    r2 = torch.deg2rad(r2)
    r3 = ((output[:, 2] + 1) / 2) * (185 - (-55)) + (-55)  # x
    r3 = torch.deg2rad(r3)
    r4 = ((output[:, 3] + 1) / 2) * (190 - (-190)) + (-190)  # y
    r4 = torch.deg2rad(r4)
    r5 = ((output[:, 4] + 1) / 2) * (115 - (-115)) + (-115)  # x
    r5 = torch.deg2rad(r5)
    r6 = ((output[:, 5] + 1) / 2) * (5 - (-5)) + (-5)  # y
    r6 = torch.deg2rad(r6)
    
    
    cos_r1 = torch.cos(r1)
    sin_r1 = torch.sin(r1)
    zeros1 = torch.zeros_like(r1)
    row1 = torch.stack([cos_r1, zeros1, sin_r1], dim=1)
    row2 = torch.stack([zeros1, torch.ones_like(r1), zeros1], dim=1)
    row3 = torch.stack([-sin_r1, zeros1, cos_r1], dim=1)
    R1 = torch.stack([row1, row2, row3], dim=1)

    cos_r2 = torch.cos(r2)
    sin_r2 = torch.sin(r2)
    zeros2 = torch.zeros_like(r2)
    row1 = torch.stack([torch.ones_like(r2), zeros2, zeros2], dim=1)
    row2 = torch.stack([zeros2, cos_r2, -sin_r2], dim=1)
    row3 = torch.stack([zeros2, sin_r2, cos_r2], dim=1)
    R2 = torch.stack([row1, row2, row3], dim=1)
    
    cos_r3 = torch.cos(r3)
    sin_r3 = torch.sin(r3)
    zeros3 = torch.zeros_like(r3)
    row1 = torch.stack([torch.ones_like(r3), zeros3, zeros3], dim=1)
    row2 = torch.stack([zeros3, cos_r3, -sin_r3], dim=1)
    row3 = torch.stack([zeros3, sin_r3, cos_r3], dim=1)
    R3 = torch.stack([row1, row2, row3], dim=1)
    
    cos_r4 = torch.cos(r4)
    sin_r4 = torch.sin(r4)
    zeros4 = torch.zeros_like(r4)
    row1 = torch.stack([cos_r4, zeros4, sin_r4], dim=1)
    row2 = torch.stack([zeros4, torch.ones_like(r4), zeros4], dim=1)
    row3 = torch.stack([-sin_r4, zeros4, cos_r4], dim=1)
    R4 = torch.stack([row1, row2, row3], dim=1)
    
    cos_r5 = torch.cos(r5)
    sin_r5 = torch.sin(r5)
    zeros5 = torch.zeros_like(r5)
    row1 = torch.stack([torch.ones_like(r5), zeros5, zeros5], dim=1)
    row2 = torch.stack([zeros5, cos_r5, -sin_r5], dim=1)
    row3 = torch.stack([zeros5, sin_r5, cos_r5], dim=1)
    R5 = torch.stack([row1, row2, row3], dim=1)
    
    cos_r6 = torch.cos(r6)
    sin_r6 = torch.sin(r6)
    zeros6 = torch.zeros_like(r6)
    row1 = torch.stack([cos_r6, zeros6, sin_r6], dim=1)
    row2 = torch.stack([zeros6, torch.ones_like(r6), zeros6], dim=1)
    row3 = torch.stack([-sin_r6, zeros6, cos_r6], dim=1)
    R6 = torch.stack([row1, row2, row3], dim=1)
    
    R0 = torch.eye(3).to(DEVICE)  # identity matrix
    
    p1_ = R0 @ p1
    p2_ = R2 @ R1 @ p2
    p3_ = R3 @ R2 @ R1 @ p3
    p4_ = R4 @ R3 @ R2 @ R1 @ p4
    p5_ = R5 @ R4 @ R3 @ R2 @ R1 @ p5
    p6_ = R6 @ R5 @ R4 @ R3 @ R2 @ R1 @ p6
    
    # print('p1: ', p1_)
    # print('p2: ', p2_)
    # print('p3: ', p3_)
    # print('p4: ', p4_)
    # print('p5: ', p5_)
    # print('p6: ', p6_)

    loss = torch.dist(x1, p1_) + torch.dist(x2, p2_) + torch.dist(x3, p3_) + torch.dist(x4, p4_) + torch.dist(x5, p5_) + torch.dist(x6, p6_)
    # print(loss)
    return loss

