import sys
import numpy as np
import cv2

INPUT_IMAGE = 'example.png'
BACKGROUND_THRESHOLD = 0.4

# INPUT_IMAGE = 'mine.png'
# BACKGROUND_THRESHOLD = 0.6

def gaussianBloom(img, background):
    backgroundBlurred = np.zeros_like(img)
    for i in range (1, 4):
        backgroundBlurred += cv2.GaussianBlur(background, (75,75), 4**i)
    imgReturn = 0.9 * img + 0.2 * backgroundBlurred
    # cv2.imshow('Background Blur Gaussian', backgroundBlurred)
    return imgReturn

def boxBloom(img, background):
    backgroundBlurred = np.zeros_like(background)
    for i in range (1, 4):
        tmpBlurred = np.copy(background)
        for j in range (3):
            tmpBlurred = cv2.blur(tmpBlurred, (15*i, 15*i))
        backgroundBlurred += tmpBlurred
    imgReturn = 0.9 * img + 0.2 * backgroundBlurred
    # cv2.imshow('Background Blur BoxBlur', backgroundBlurred)
    return imgReturn


def main():

    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    cv2.imshow('No Effect', img)
    if img is None:
        print('Cannot open image')
        sys.exit()

    img = np.float32(img) / 255

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBackground = np.copy(img)

    for y in range (len(img)):
        for x in range (len(img[0])):
            if imgGray[y, x] < BACKGROUND_THRESHOLD:
                imgBackground[y, x] = 0
    # cv2.imshow('Background', imgBackground)

    boxFinal = boxBloom(img, imgBackground)
    gaussianFinal = gaussianBloom(img, imgBackground)

    cv2.imshow('Gaussian Bloom', gaussianFinal)
    cv2.imwrite ('01 - Gaussian.png', gaussianFinal*255)
    cv2.imshow('Box Bloom', boxFinal)
    cv2.imwrite ('02 - Box Bloom.png', boxFinal*255)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()