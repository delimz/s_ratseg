import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import cytomine

import sys
print sys.argv[1:]

print(tf.test.is_gpu_available())
print(cv2.__version__)
print(cytomine.__version__)
print("yeay")
