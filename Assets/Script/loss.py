import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import math


MSE = nn.MSELoss(reduction='sum')
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def calc_degree(y, output):
    # print('y: ', y)
    # print('real output: ',output) # grad
    # print('--------',output[:, :, 0])
    # print('=======', y[:, 0])
    r1 = ((output[:, 0] + 1) / 2) * (165 - (-165)) + (-165)
    r2 = ((output[:, 1] + 1) / 2) * (85 - (-125)) + (-125) 
    r3 = ((output[:, 2] + 1) / 2) * (185 - (-55)) + (-55)
    r4 = ((output[:, 3] + 1) / 2) * (190 - (-190)) + (-190)
    r5 = ((output[:, 4] + 1) / 2) * (115 - (-115)) + (-115)
    r6 = y[:, 5]
    
    deg1 = torch.abs(y[:, 0] - r1)
    deg5 = torch.abs(y[:, 4] - r5)
    return deg1, deg5


def calc_distance(x, y, output):   
# 6 axis robot coordinate
    x1 = x[0][-1][0:3]
    x2 = x[0][-1][3:6]
    x3 = x[0][-1][6:9]
    x4 = x[0][-1][9:12]
    x5 = x[0][-1][12:15]
    x6 = x[0][-1][15:18]

# hiwin 6 axis robot coordinate
    p1 = torch.tensor([0.0, 0, 0.0]).to(DEVICE)
    p2 = torch.tensor([0.0, 0.55, 0.0]).to(DEVICE)
    p3 = torch.tensor([0.0, 0.55, -0.025]).to(DEVICE)
    p4 = torch.tensor([0.0, 0.55, -0.175]).to(DEVICE)
    p5 = torch.tensor([0.0, 0.55, -0.375]).to(DEVICE)
    p6 = torch.tensor([0.0, 0.55, -0.45]).to(DEVICE)
    
    v1 = torch.tensor([0.0, 0.0, 0.0]).to(DEVICE)
    v2 = torch.tensor([0.0, 0.55, 0.0]).to(DEVICE)
    v3 = torch.tensor([0.0, 0.0, -0.025]).to(DEVICE)
    v4 = torch.tensor([0.0, 0.0, -0.15]).to(DEVICE)
    v5 = torch.tensor([0.0, 0.0, -0.2]).to(DEVICE)
    v6 = torch.tensor([0.0, 0.0, -0.075]).to(DEVICE)
    
    # dnn
    # r1 = ((output[:, :, 0] + 1) / 2) * (165 - (-165)) + (-165) 
    # r1 = torch.deg2rad(r1)
    # r2 = ((output[:, :, 1] + 1) / 2) * (85 - (-125)) + (-125) 
    # r2 = torch.deg2rad(r2)
    # r3 = ((output[:, :, 2] + 1) / 2) * (185 - (-55)) + (-55)
    # r3 = torch.deg2rad(r3)
    # r4 = ((output[:, :, 3] + 1) / 2) * (190 - (-190)) + (-190)
    # r4 = torch.deg2rad(r4)
    # r5 = ((output[:, :, 4] + 1) / 2) * (115 - (-115)) + (-115) 
    # r5 = torch.deg2rad(r5)
    # r6 = y[:, 5]
    # r6 = torch.deg2rad(r6)

    # lstm
    r1 = ((output[:, 0] + 1) / 2) * (165 - (-165)) + (-165)
    r1 = torch.deg2rad(r1)
    r2 = ((output[:, 1] + 1) / 2) * (85 - (-125)) + (-125) 
    r2 = torch.deg2rad(r2)
    r3 = ((output[:, 2] + 1) / 2) * (185 - (-55)) + (-55)
    r3 = torch.deg2rad(r3)
    r4 = ((output[:, 3] + 1) / 2) * (190 - (-190)) + (-190)
    r4 = torch.deg2rad(r4)
    r5 = ((output[:, 4] + 1) / 2) * (115 - (-115)) + (-115)
    r5 = torch.deg2rad(r5)
    r6 = y[:, 5]
    r6 = torch.deg2rad(r6)
    
    # R1: 繞 y 軸 / R2: x / R3: x / R4: y / R5: x / R6: y
    R1 = rot_y(r1)
    R2 = rot_x(r2)
    R3 = rot_x(r3)
    R4 = rot_z(r4)
    R5 = rot_x(r5)
    R6 = rot_z(r6)
    
    v1_ = R1 @ v1
    p1_ = v1_
    v2_ = R1 @ (R2 @ v2)
    p2_ = p1_ + v2_
    v3_ = R1 @ (R2 @ (R3 @ v3))
    p3_ = p2_ + v3_
    v4_ = R1 @ (R2 @ (R3 @ v4))
    p4_ = p3_ + v4_
    v5_ = R1 @ (R2 @ (R3 @ (R4 @ (R5 @ v5))))
    p5_ = p4_ + v5_
    v6_ = R1 @ (R2 @ (R3 @ (R4 @ (R5 @ v6))))
    p6_ = p5_ + v6_

    set1_points = torch.cat([x1, x2, x3, x4, x5, x6]).reshape(6,3)
    set2_points = torch.cat([p1_, p2_, p3_, p4_, p5_, p6_]).reshape(6,3)
    total_points = 50

    num_intervals_set1 = set1_points.size(0) - 1
    num_intervals_set2 = set2_points.size(0) - 1

    num_points_per_interval_set1 = total_points // num_intervals_set1
    num_points_per_interval_set2 = total_points // num_intervals_set2

    remaining_points_set1 = total_points - (num_points_per_interval_set1 * num_intervals_set1)
    remaining_points_set2 = total_points - (num_points_per_interval_set2 * num_intervals_set2)

    interpolated_set1 = []
    for i in range(num_intervals_set1):
        start_point = set1_points[i]
        end_point = set1_points[i + 1]
        num_points = num_points_per_interval_set1 + (1 if i < remaining_points_set1 else 0)
        weights = torch.linspace(0, 1, num_points).unsqueeze(1)
        interpolated = torch.lerp(start_point, end_point, weights.to(DEVICE))
        interpolated_set1.append(interpolated)
    interpolated_set1 = torch.cat(interpolated_set1)

    interpolated_set2 = []
    for i in range(num_intervals_set2):
        start_point = set2_points[i]
        end_point = set2_points[i + 1]
        num_points = num_points_per_interval_set2 + (1 if i < remaining_points_set2 else 0)
        weights = torch.linspace(0, 1, num_points).unsqueeze(1)
        interpolated = torch.lerp(start_point, end_point, weights.to(DEVICE))
        interpolated_set2.append(interpolated)
    interpolated_set2 = torch.cat(interpolated_set2)
    
    distance = MSE(interpolated_set1, interpolated_set2)
    
    dist6 = torch.norm(x6 - p6_)
    loss_ = distance/50 + dist6*5
    return loss_, dist6



def rot_x(rad):
    cos_ = torch.cos(rad)
    sin_ = torch.sin(rad)
    zero = torch.zeros_like(rad)
    row1 = torch.stack([torch.ones_like(rad), zero, zero], dim=0).squeeze()
    row2 = torch.stack([zero, cos_, sin_], dim=0).squeeze()
    row3 = torch.stack([zero, -sin_, cos_], dim=0).squeeze()
    Rx = torch.stack([row1, row2, row3], dim=1).to(DEVICE)
    return Rx
    
def rot_y(rad):
    cos_ = torch.cos(rad)
    sin_ = torch.sin(rad)
    zero = torch.zeros_like(rad)
    row1 = torch.stack([cos_, zero, -sin_], dim=0).squeeze()
    row2 = torch.stack([zero, torch.ones_like(rad), zero], dim=0).squeeze()
    row3 = torch.stack([sin_, zero, cos_], dim=0).squeeze()
    Ry = torch.stack([row1, row2, row3], dim=1).to(DEVICE)
    return Ry
    
def rot_z(rad):
    cos_ = torch.cos(rad)
    sin_ = torch.sin(rad)
    zero = torch.zeros_like(rad)
    row1 = torch.stack([cos_, -sin_, zero], dim=0).squeeze()
    row2 = torch.stack([sin_, cos_, zero], dim=0).squeeze()
    row3 = torch.stack([zero, zero, torch.ones_like(rad)], dim=0).squeeze()
    Rz = torch.stack([row1, row2, row3], dim=1).to(DEVICE)
    return Rz

# if __name__=='__main__':
#     calc()