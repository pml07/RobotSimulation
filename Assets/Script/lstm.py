import torch
import torch.nn as nn


class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm1 = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.lstm2 = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True)

        self.fc = nn.Linear(hidden_size, output_size)
        self.activate = nn.Tanh()
    
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, _ = self.lstm1(x, (h0, c0))
        out, _ = self.lstm2(out, (h0, c0))
        out = out[:, -1, :]

        out = self.fc(out)
        out = self.activate(out)        
        return out


if __name__ == "__main__":
    DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = LSTM(input_size=18, hidden_size1=32, hidden_size2=32, output_size=6, num_layers=2).to('cuda:0')
    
    x = torch.randn(1, 6, 18).to(DEVICE)
    target = torch.randn(1,6).to(DEVICE)

    output = model(x)
    MSE = nn.MSELoss()
    loss = MSE(output, target)
    loss.backward()
    for name, p in model.named_parameters():
        print(name, 'gradient is', p.grad)
    
    
