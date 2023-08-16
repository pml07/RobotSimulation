import pickle
import numpy as np
import os, re, random
import torch
import matplotlib.pyplot as plt
import train


def get_data(dataset, dir, ca): # for train 
    filepath = os.path.join("../DataSet", dataset, dir)
    files = os.listdir(filepath)
    files.sort()
    traindatas = []
    ca = ca.split("_")
    for file in files:
        if re.split("_|\.", file)[-2] in ca:
            with open(os.path.join(filepath, file), 'rb') as f:
                data = pickle.load(f)
            for i in range(0, len(data)):
                input_data = np.array(data[i:i+1, :18])
                output_data =  np.array(data[i, 18:])
                traindatas.append((input_data, output_data))

    data = {"x":[], "y":[]}
    for i, (x,y) in enumerate(traindatas):
        data["x"].append(torch.tensor(x.astype("float32")))
        data["y"].append(torch.tensor(y.astype("float32")))
    data["x"] = torch.nn.utils.rnn.pad_sequence(data["x"], batch_first=True, padding_value=0) # pad
    data["y"] = torch.nn.utils.rnn.pad_sequence(data["y"], batch_first=True, padding_value=0)
    return data

def get_single_data(dir, filename, file):
    datas = []
    if dir != "":
        filepath = os.path.join("../DataSet", dir, filename, file)
    else:
        filepath = os.path.join("../DataSet", file)

    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    for i in range(0, len(data)):
        input_data = np.array(data[i, :18])
        datas.append(input_data)
    return datas


if __name__ == '__main__':
    dir = 'normalize'
    filename = 'train'
    train_ca = '01'

    train_data = get_data(dir, filename, ca=train_ca)