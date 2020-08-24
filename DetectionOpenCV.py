import cv2
import numpy as np
import imutils

class DetectionOpenCV():
    def __init__(self, _SizeMax = 5000, _SizeMin = 900, _ResizeWidth = 620, _ResizeHeight = 480, _CannyThreshold1 = 30, _CannyThreshold2 = 200):
        self.sizeMax = _SizeMax                     # Kích thước ước lượng biển số lớn nhất trong ảnh
        self.sizeMin = _SizeMin                     # Kích thước ước lượng biển số nhỏ nhất trong ảnh
        self.resizeWidth = _ResizeWidth             # Chiều rộng resize ảnh
        self.resizeHeight = _ResizeHeight           # Chiều rộng resize ảnh
        self.cannyThreshold1 = _CannyThreshold1     # Ngưỡng 1 phát hiện cạnh biên canny
        self.cannyThreshold2 = _CannyThreshold2     # Ngưỡng 2 phát hiện cạnh biên canny
    
    def detection(self, _ImgInput):
        # Param
        max_size = self.sizeMax
        min_size = self.sizeMin

        # Resize image
        img = cv2.resize(_ImgInput, (self.resizeWidth, self.resizeHeight))

        # Edge detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                        # convert to grey scale
        gray = cv2.bilateralFilter(gray, 11, 17, 17)                                        # Blur to reduce noise
        edged = cv2.Canny(gray, self.cannyThreshold1, self.cannyThreshold2)                 # Perform Edge detection

        # Find contours in the edged image, keep only the largest ones, and initialize our screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        screenCnt = None

        # Loop over our contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05 * peri, True)

            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4 and max_size > cv2.contourArea(c) > min_size:
                screenCnt = approx
                break

        img_plate = np.array([])    
        if screenCnt is None:
            detected = 0
            return 0, img_plate
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

            # Masking the part other than the number plate
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
            new_image = cv2.bitwise_and(img, img, mask=mask)

            # Now crop
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            img_plate = gray[topx:bottomx + 1, topy:bottomy + 1]
            return 1, img_plate