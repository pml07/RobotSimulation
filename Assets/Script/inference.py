import pickle
import numpy as np
import argparse
from pathlib import Path
import os
from tqdm import tqdm
from processing import get_single_data
import torch
import socket

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

def send(out):
    rot_values = [str(round(rot.item(), 4)) for rot in out]
    send_msg = ','.join(rot_values)
    s_socket.sendall(send_msg.encode())

def receive():
    message = s_socket.recv(1024)
    message = message.decode('utf-8')
    msg = [float(val) for tpl in message.split(";") for val in tpl.strip("()").split(",")]
    # print(msg)
    return msg
    
    
def main(): 
    data = load_data(file)
    model = load_model()
    for line in data:
        data_tensor = torch.tensor(line).float().unsqueeze(0).unsqueeze(0).to(DEVICE)
        # print(data_tensor)
        output, mean, log_var = model(data_tensor)
        for out in output:
            send(out)
            msg = receive()
            # print(msg)
    print('Finish!')        

if __name__ == '__main__':
    TCP_IP = '127.0.0.1'
    TCP_PORT = 8080

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen()
    s_socket, addr = s.accept()
    print("conected to client")
    
    main()
    
    s.close()
