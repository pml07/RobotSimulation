import torch
import torch.nn as nn

class DNN(nn.Module):
    def __init__(self):
        super(DNN, self).__init__()
        
        self.fc1 = nn.Linear(18, 32)
        self.relu1 = nn.ReLU()
        
        self.fc2 = nn.Linear(32, 32)
        self.relu2 = nn.ReLU()
        
        self.fc3 = nn.Linear(32, 5)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        
        x = self.fc2(x)
        x = self.relu2(x)
        
        x = self.fc3(x)
        x = self.tanh(x)
        return x