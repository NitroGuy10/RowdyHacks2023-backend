import cv2
import dlib
import numpy as np

# Load the two images
img1 = cv2.imread('ashrita.png')
img2 = cv2.imread('harshitha.png')



# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


# Detect faces and landmarks in both images
face1 = detector(img1)[0]
face2 = detector(img2)[0]
landmarks1 = predictor(img1, face1)
landmarks2 = predictor(img2, face2)

# Extract landmark coordinates as numpy arrays
landmarks1 = np.array([[p.x, p.y] for p in landmarks1.parts()])
landmarks2 = np.array([[p.x, p.y] for p in landmarks2.parts()])

# Calculate affine transformation matrix
M, _ = cv2.estimateAffinePartial2D(landmarks1, landmarks2)

# Apply affine transformation to image 1
aligned_img1 = cv2.warpAffine(img1, M, img2.shape[:2][::-1])

# Merge images using alpha blending
alpha = 0.5
result = cv2.addWeighted(aligned_img1, alpha, img2, 1-alpha, 0)

# Display the merged image
cv2.imshow('Merged Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
