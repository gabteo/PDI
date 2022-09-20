import numpy as np
import cv2

INPUT_IMAGE = 'example.png'
BACKGROUND_THRESHOLD = 0.3

def main():

    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    img = img.astype(np.float32)
    img /= 255

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBackground = np.copy(img)

    for y in range (len(img)):
        for x in range (len(img[0])):
            if imgGray[y, x] > BACKGROUND_THRESHOLD:
                imgBackground[y, x] = 0

    imgBackgroundGauss = cv2.GaussianBlur(imgBackground, (25,25), 2)
    imgBackgroundGauss += cv2.GaussianBlur(imgBackgroundGauss, (25,25), 4)
    imgBackgroundGauss += cv2.GaussianBlur(imgBackgroundGauss, (25,25), 8)

    imgFinal = 0.9 * img + 0.1 * imgBackgroundGauss

    imgFinal = np.where(imgFinal > 1, 1, imgFinal)

    cv2.imshow('Example', img)
    cv2.imshow('Example Final', imgFinal)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()