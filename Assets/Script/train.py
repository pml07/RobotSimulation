import torch
import torch.nn as nn
from torch.optim import Adam
import torch.optim as optim
from torch.utils.data import DataLoader, SubsetRandomSampler, TensorDataset
from tqdm import tqdm
import numpy as np
import os
import json, pickle
import dnn, lstm, processing, loss
import matplotlib.pyplot as plt

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

dataset = 'demo'
train_dir = 'train'
train_ca = '0'
test_dir = 'test'
test_ca = '1'
batch_size = 1
save_path = os.path.join("ckpt", f"6to6_{dataset}_{train_dir}_{train_ca}")
epochs = 300
lr = 0.000001
best_loss = 100

    
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
    model = dnn.DNN()
    # model = lstm.LSTM(input_size=15, hidden_size=16, output_size=4, num_layers=1).to(DEVICE)
    # model = torch.load('ckpt/6to6_demo_train_0/best.pth')
    model = model.to(DEVICE)
    print('------model: ',model)
    return model


def train(model, train_, test_, early_stop_patience=15, delta=100):
    best_loss = 100
    optimizer = Adam(model.parameters(), lr=lr)
    # scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.9)
    lossList = []
    model_path = f"{save_path}"
    if not os.path.isdir(model_path):
        os.mkdir(model_path)
    
    no_improvement = 0
    # training
    for epoch in range(epochs):
        # train
        train_lossList = []
        dist6_train = []
        deg1_train = []
        deg5_train = []
        model.train()
        for i, (x, y) in enumerate(tqdm(train_)):
            x = x.to(DEVICE)
            y = y.to(DEVICE)
            # print('---------------x: ', x)
            # print('y: ', y)
            optimizer.zero_grad()
            output = model(x)
            dist, dist6 = loss.calc_distance(x, y, output)  # distance
            deg1, deg5 = loss.calc_degree(y, output)  # degree
            
            loss_ = dist*100 + deg1 + deg5  # loss weight 要試
            train_lossList.append(loss_)
            dist6_train.append(dist6)

            loss_.backward()
            optimizer.step()
            # for name, p in model.named_parameters():
            #     print(name, 'gradient is', p.grad)
        train_loss = sum(train_lossList) / len(train_lossList)
        dist6_loss = sum(dist6_train) / len(dist6_train)
        deg1_loss = sum(deg1_train) / len(deg1_train)
        deg5_loss = sum(deg5_train) / len(deg5_train)
        robot_loss = "dist6 = {}, deg1 = {}, deg5 = {}".format(dist6_loss.item(), deg1_loss.item(), deg5_loss.item())
        with open(f"output/training_loss.txt", "a") as f:
            f.write(robot_loss)
            f.write("\n")

        # scheduler.step()

        # test
        test_lossList = []
        dist6_test = []
        deg1_test = []
        deg5_test = []
        model.eval()
        with torch.no_grad():
            for i, (x, y) in enumerate(tqdm(test_)):
                x = x.to(DEVICE)
                y = y.to(DEVICE)

                output = model(x)
                dist, dist6 = loss.calc_distance(x, y,output)  # distance
                deg1, deg5 = loss.calc_degree(y, output)  # degree

                loss_ = dist*100 + deg1 + deg5  # loss 權重自己試
                test_lossList.append(loss_)
                dist6_test.append(dist6)
                deg1_test.append(deg1)
                deg5_test.append(deg5)
            test_loss = sum(test_lossList) / len(test_lossList)
            dist6_loss = sum(dist6_test) / len(dist6_test)
            deg1_loss = sum(deg1_test) / len(deg1_test)
            deg5_loss = sum(deg5_test) / len(deg5_test)
            robot_loss = "dist6 = {}, deg1 = {}, deg5 = {}".format(dist6_loss.item(), deg1_loss.item(), deg5_loss.item())
            with open(f"output/test_loss.txt", "a") as f:
                f.write(robot_loss)
                f.write("\n")
                
        # save model
        if test_loss < best_loss:
            torch.save(model, model_path + "/best.pth")
            best_loss = test_loss
        else:
            torch.save(model, model_path + "/last.pth")
        
        # early stopping
        if (test_loss - train_loss) > delta:
            no_improvement += 1
        else:
            no_improvement += 0
        if no_improvement >= early_stop_patience:
            print(f"No improvement for {early_stop_patience} epochs. Early stopping.")
            break
        
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
    plt.ylabel("Loss (deg)")
    plt.title("Loss")
    plt.legend()
    plt.savefig(save_path + "/loss.png")
     

if __name__=='__main__':
    # save log
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
        opt = {"dataset":dataset, "train_dir":train_dir, "train_ca":train_ca, "test_ca":test_ca, 
                "lr":lr, "batch_size":batch_size, "epochs":epochs}
        with open(save_path + '/opt.json', 'w') as fp:
            json.dump(opt, fp)
    # train
    model = load_model()
    train_, test_, train_sampler, test_sampler = load_data()
    train(model, train_, test_)
    plot()