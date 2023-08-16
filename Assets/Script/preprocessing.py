import json, pickle
import numpy as np
import math

if __name__ == "__main__":
    file = '../DataSet/demo/demo_13'
    
    Joint = ["j1x", "j1y", "j1z", "j2x", "j2y", "j2z", "j3x", "j3y", "j3z", "j4x", "j4y", "j4z", "j5x", "j5y", "j5z", "j6x", "j6y", "j6z"]
    
    content = []    
    
    with open(f'{file}.json', 'rb') as fjson:
        lines = fjson.readlines()
        total_lines = len(lines)
        split_index = int(total_lines * 0.8)
        
        for i, line in enumerate(lines):
            data = json.loads(line)
            coor = np.zeros(18)
            
            for j, item in enumerate(Joint):
                if item in data.keys():
                    coor[j] = float(data[item])
            
            content.append(coor)
            
            if i == split_index:
                with open(f'{file}0.pkl', 'wb') as fpickle_train:
                    pickle.dump(np.array(content), fpickle_train)
                
                content = []
        
        with open(f'{file}1.pkl', 'wb') as fpickle_test:
            pickle.dump(np.array(content), fpickle_test)

