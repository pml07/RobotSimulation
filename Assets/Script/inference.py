import pickle
import numpy as np
import argparse
from pathlib import Path
import os
from tqdm import tqdm
from processing import get_single_data
import torch
# import socket

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str, help="Model path", required=True)
parser.add_argument("-d", "--dataset", type=str, help="Dataset Dir", required=True)
parser.add_argument("-f", "--file", type=str, help="File Path")
args = parser.parse_args()

dataset = args.dataset.split('/')[0]
dir = args.dataset.split('/')[1]
file = args.file


def load_model():
    print(">>> Model loaded -->")
    path = os.path.join("ckpt", args.model)
    model = torch.load(path + "/best.pth").to(DEVICE)
    model.eval()
    return model

def load_data(file):
    print(">>> Data loaded -->", file)
    data = get_single_data(dataset, dir, file)
    return data

# def send(out):
#     rot_values = [str(round(rot.item(), 4)) for rot in out]
#     send_msg = ','.join(rot_values)
#     send_socket.sendall(send_msg.encode())

# def receive():
#     message = receive_socket.recv(1024)
#     message = message.decode('utf-8')
#     msg = [float(val) for tpl in message.split(";") for val in tpl.strip("()").split(",")]
#     # print(msg)
#     return msg
    
    
def main(): 
    path = os.path.join("ckpt", args.model)
    data = load_data(file)
    model = load_model()
    for line in data:
        print('original input: ', line)
        data_tensor = torch.tensor(line[0:15]).float().unsqueeze(0).unsqueeze(0).to(DEVICE)
        print('model input: ', data_tensor)
        output = model(data_tensor)
        print('output: ', output)
        output = output.tolist()[0]
        j1 = ((output[0] + 1) / 2) * (165 - (-165)) + (-165)
        j2 = ((output[1] + 1) / 2) * (85 - (-125)) + (-125) 
        j3 = ((output[2] + 1) / 2) * (185 - (-55)) + (-55)
        j4 = ((output[3] + 1) / 2) * (190 - (-190)) + (-190)
        j5 = ((output[4] + 1) / 2) * (115 - (-115)) + (-115)
        j6 = line[19]
        
        out = "rot1 = {}, rot2 = {}, rot3 = {}, rot4 = {}, rot5 = {}, rot6 = {}".format(j1, j2, j3, j4, j5, j6)
        with open(path + "_predict.txt", "a") as f:
            f.write(out)
            f.write("\n")
            
    print('Finish!')        

if __name__ == '__main__':
    # UDP_IP = '127.0.0.1'
    # UDP_SEND_PORT = 5065
    # UDP_RECEIVE_PORT = 5066

    # send_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # receive_socket.bind((UDP_IP, UDP_RECEIVE_PORT))
    
    main()