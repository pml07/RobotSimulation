import json, pickle
import numpy as np


if __name__ == "__main__":

    file = '../DataSet/pos/joint_06'
    
    # Joint = ["lshoulder.x", "lshoulder.y", "lshoulder.z", "rshoulder.x", "rshoulder.y", "rshoulder.z",
    #         "rarm.x", "rarm.y", "rarm.z", "rforearm.x", "rforearm.y", "rforearm.z", "rhand.x", "rhand.y", "rhand.z",
    #         "rindex.x", "rindex.y", "rindex.z"]
    Joint = ["j1x", "j1y", "j1z", "j2x", "j2y", "j2z", "j3x", "j3y", "j3z", "j4x", "j4y", "j4z", "j5x", "j5y", "j5z", "j6x", "j6y", "j6z",
            "rot1", "rot2", "rot3", "rot4", "rot5", "rot6"]
    content = []
    with open(f'{file}.json','rb') as fjson:
        for line in fjson.readlines():
            data = json.loads(line)
            coor = np.zeros(24)
            # lshoulder_x = float(data["lshoulder.x"])
            # lshoulder_y = float(data["lshoulder.y"])
            # lshoulder_z = float(data["lshoulder.z"])
            # for i, item in enumerate(Joint):
            #     if item in data.keys():
            #         if item[-1] == 'x':
            #             coor[i] = float(data[item]) - lshoulder_x
                        
            #         elif item[-1] == 'y':
            #             coor[i] = float(data[item]) - lshoulder_y
            #         else:
            #             coor[i] = float(data[item]) - lshoulder_z
            for i, item in enumerate(Joint):
                coor[i] = float(data[item])
            content.append(coor)
    content = np.array(content)

    with open (f'{file}.pkl','wb') as fpickle:
        pickle.dump(content, fpickle)



