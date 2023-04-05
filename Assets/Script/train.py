import torch
import torch.nn as nn
from torch.optim import Adam
import torch.optim as optim
from torch.utils.data import DataLoader, SubsetRandomSampler, TensorDataset
from tqdm import tqdm
import numpy as np
import os
import json, pickle
import lstm, processing, loss
import socket
import matplotlib.pyplot as plt

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
dataset = 'random'  # test 1 / 2
train_dir = 'train'
train_ca = '0'  # 10: -5~5 / 12
test_dir = 'test'
test_ca = '1'  # 11: -5~5 / 13
batch_size = 1
save_path = os.path.join("ckpt", f"{dataset}_{train_dir}_{train_ca}")
epochs = 50
lr = 0.00001 # 0.00001
best_loss = 1000


def send(output):
    rot_values = output.tolist()[0]
    send_msg = ','.join(str(f) for f in rot_values)
    # print("------send: ", send_msg)
    s_socket.sendall(send_msg.encode())
    
def receive():
    message = s_socket.recv(1024)
    message = message.decode('utf-8')  # string
    msg = [float(val) for tpl in message.split(";") for val in tpl.strip("()").split(",")] # list[float]
    # print(msg)
    r_pos = torch.tensor([msg], requires_grad=True)
    # print('r_pos: ', r_pos)
    return r_pos


def save_result(save_path, result):
    with open(save_path + "/result.txt" , "a") as f:
        f.write(result)
        f.write("\n")

    
def load_data():
    validation_split = 0.2
    shuffle_dataset = True
    random_seed = 42
    # get data
    train_data = processing.get_data(dataset, train_dir, ca=train_ca)   
    test_data = processing.get_data(dataset, test_dir, ca=test_ca)
    dataset_size = len(train_data['x'])
    indices = list(range(dataset_size))
    split = int(np.floor(validation_split * dataset_size))
    if shuffle_dataset:
        np.random.seed(random_seed)
        np.random.shuffle(indices)
    train_indices, test_indices = indices[split:], indices[:split]
    train_sampler = SubsetRandomSampler(train_indices)
    test_sampler = SubsetRandomSampler(test_indices)
    
    train_ = DataLoader(dataset=TensorDataset(train_data["x"], train_data["y"]), batch_size=batch_size, shuffle=True)
    test_ = DataLoader(dataset=TensorDataset(test_data["x"], test_data["y"]), batch_size=batch_size, shuffle=True) 
    return train_, test_, train_sampler, test_sampler

def load_model():
    model = lstm.LSTM(input_size=18, hidden_size=32, output_size=6, num_layers=1).to(DEVICE)
    model = model.to(DEVICE)
    print('------model: ',model)
    return model


def train(model, train_, test_):
    best_loss = 1000
    optimizer = Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.9)
    lossList = []
    model_path = f"{save_path}"
    if not os.path.isdir(model_path):
        os.mkdir(model_path)
    
    # training
    for epoch in range(epochs):
        # train
        train_lossList = []
        model.train()
        for i, (x, y) in enumerate(tqdm(train_)):
            x = x.to(DEVICE)
            y = y.to(DEVICE)
            optimizer.zero_grad()
            output = model(x)
            # print('---------------y: ', y)
            # print('---------------output: ', output)
            send(output)
            r_pos = receive()
            
            # print('-----------------r_pos: ', r_pos)
            loss_ = loss.total_loss(y, output) # output
            train_lossList.append(loss_)
            loss_.backward()
            optimizer.step()
            # for name, p in model.named_parameters():
            #     print(name, 'gradient is', p.grad)
        
        train_loss = sum(train_lossList) / len(train_lossList)
        scheduler.step()

        # test
        test_lossList = []
        model.eval()
        with torch.no_grad():
            for i, (x, y) in enumerate(tqdm(test_)):
                x = x.to(DEVICE)
                y = y.to(DEVICE)
                output = model(x)
                send(output)
                r_pos = receive()
                loss_ = loss.loss_(y, output) # output
                test_lossList.append(loss_)
            test_loss = sum(test_lossList) / len(test_lossList)
                
        # save model
        if train_loss < best_loss:
            torch.save(model, model_path + "/best.pth")
            best_loss = train_loss
        else:
            torch.save(model, model_path + "/last.pth")
        result = "Epoch = {:3}/{}, train_loss = {:8}, test_loss = {:8}".format(epoch+1, epochs, train_loss.item(), test_loss.item())
        lossList.append([train_loss.item(), test_loss.item()])
        print(result)
        save_result(model_path, result)
    with open(model_path + '/loss.pkl', 'wb')as fpick:
        pickle.dump(lossList, fpick)    
    print("Done!")
    
def plot():
    epochs = []
    train_losses = []
    test_losses = []
    
    with open(save_path + "/result.txt", "r") as f:
        for line in f:
            parts = line.strip().split(", ")
            epoch, total_epochs = map(int, parts[0].split("=")[-1].split("/"))
            train_loss = float(parts[1].split("=")[-1])
            test_loss = float(parts[2].split("=")[-1])
            epochs.append(epoch)
            train_losses.append(train_loss)
            test_losses.append(test_loss)
    
    # Create plot
    plt.plot(epochs, train_losses, label="Training Loss")
    plt.plot(epochs, test_losses, label="Test Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Loss")
    plt.legend()
    plt.savefig(save_path + "/loss.png")
     

if __name__=='__main__':
    TCP_IP = 'localhost'
    TCP_PORT = 8080

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen()
    s_socket, addr = s.accept()
    print("connected to client")

    # save log
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
        opt = {"dataset":dataset, "train_dir":train_dir, "train_ca":train_ca, "test_ca":test_ca, 
                "lr":lr, "batch_size":batch_size, "epochs":epochs}
        with open(save_path + '/opt.json', 'w') as fp:
            json.dump(opt, fp)
    try:
        train
        model = load_model()
        train_, test_, train_sampler, test_sampler = load_data()
        train(model, train_, test_)

        plot()
    except(KeyboardInterrupt):
        s.close()
