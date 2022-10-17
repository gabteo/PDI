from pickletools import uint8
import numpy as np
import cv2

INPUT_IMAGE = '205.bmp'

def main():
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    # img = img.astype(np.float32) / 255
    print(img)
    cv2.imshow('IMG', img)

    # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # (a, imgBinary) = cv2.threshold(imgGray, 0.8, 1, cv2.THRESH_BINARY)
    # cv2.imshow('IMG Binary', imgBinary)

    # gX = cv2.Sobel(imgGray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=3)
    # gY = cv2.Sobel(imgGray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=3)
    # imgBorder = gX * 0.5 + gY * 0.5

    # cv2.imshow('Sobel', imgBorder)


    imgCanny = cv2.Canny(img, 100, 255)
    cv2.imshow('Canny', imgCanny)

    kernel = np.ones((5, 5))
    dilatation = cv2.dilate(imgCanny, kernel, iterations=1)
    closing = cv2.erode(dilatation, kernel, iterations=1)

    cv2.imshow('Closing', closing)

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()