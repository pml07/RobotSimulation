import numpy as np
import math

# angle
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def cross(v1,v2):
  return np.cross(v1,v2)

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
#   return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
    return np.arccos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def test(angle, v1, v2):
    R_M = [[np.cos((np.pi * angle) / 180), -np.sin((np.pi * angle) / 180)],
            [np.sin((np.pi * angle) / 180), np.cos((np.pi * angle) / 180)]]
    if np.dot(v2, np.dot(R_M, v1)) > np.dot(v2, np.dot(np.transpose(R_M), v1)):
        return "positive"
    return "negative"

a = (1,1)
b = (-2,1)
c = (1,-2)
# print(angle(b,a))
a1 = math.degrees(angle(c,a))
print(dotproduct(c,a))
print(a1)
print(test(a1, c, a))