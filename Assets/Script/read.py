import pickle
import matplotlib.pyplot as plt
import numpy as np

with open('../DataSet/pos/train/joint_05.pkl', 'rb') as f:
    data = pickle.load(f)
print(data[0])
    
# data = np.array(data)

# fig, ax = plt.subplots(figsize=(8, 6))
# for i in range(data.shape[1]):
#     ax.plot(data[:, i], label=f"Dim {i}")

# ax.legend()
# ax.set_xlabel("Frames")
# ax.set_ylabel("Value")
# ax.set_title("Plot of data dimensions")
# plt.savefig("../DataSet/data.png")
    
