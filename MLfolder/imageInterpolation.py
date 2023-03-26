import cv2
import numpy as np

# Load the two images
img1 = cv2.imread('image1.png')
img2 = cv2.imread('image2.png')

# Choose a set of corresponding points on each image
points1 = np.array([[x1, y1], [x2, y2], ...])
points2 = np.array([[x1, y1], [x2, y2], ...])

# Calculate the transformation matrix
M = cv2.estimateAffinePartial2D(points1, points2)[0]

# Generate a series of intermediate images
num_steps = 10
for i in range(num_steps):
    alpha = i / float(num_steps)
    interpolated_img = cv2.addWeighted(img1, 1 - alpha, cv2.warpAffine(img1, M, img1.shape[1::-1]), alpha, 0)
    cv2.imwrite('interpolation_step_{}.png'.format(i), interpolated_img)