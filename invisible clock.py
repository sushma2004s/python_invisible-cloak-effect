import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
time.sleep(2)

background = 0
for i in range(50):   # Corrected (removed ;)
    ret, background = cap.read()

background = np.flip(background, axis=1)   # Flip for consistency

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = np.flip(img, axis=1)

    # Convert frame to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Red color range 1
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # Red color range 2
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Combine masks
    mask1 = mask1 + mask2

    # Morphological operations to clean noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=1)

    # Invert mask
    mask2 = cv2.bitwise_not(mask1)

    # Segment the cloak (red part) and background
    res1 = cv2.bitwise_and(background, background, mask=mask1)
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    # Merge both
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("Magic", final_output)

    # Press ESC to exit
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
