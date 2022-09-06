import sys
import timeit
import numpy as np
import cv2

INPUT_IMAGE =  'arroz.bmp'

def blurh(img, fullw):
    w = fullw//2
    img_return = np.array
    img_return = img.reshape((img.shape[0], img.shape[1], 1))

    for y in range(w, len(img)-w):
        for x in range(w, len(img[0])-w):
            soma = 0
            for i in range(-w, w+1):
                for j in range(-w, w+1):
                    soma += img[y+i, x+j]
            media = soma / fullw**2
            img_return[y, x] = media

    return img_return

def chadBlur(img, fullw):
    w = fullw//2

    img_return = np.array
    img_return = img.reshape((img.shape[0], img.shape[1], 1))

    for y in range(w, len(img)-w):
        soma = 0
        for x in range(w, len(img[0])-w):
            if (x == w):                
                for i in range(-w, w+1):
                    for j in range(-w, w+1):
                        soma += img[y+i, w+j]
                img_return[y, x] = soma/fullw**2
                pass
            for k in range(-w, w+1):
                soma += img[y+k, x+w]
                soma -= img[y+k, x-w-1]
            media = soma / fullw**2
            img_return[y, x] = media

    return img_return
img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)

if img is None:
    print('Cannot open image')
    sys.exit()

img = img.reshape((img.shape[0], img.shape[1], 1))
img = img.astype(np.float32) / 255

# print(type (img))
# img_output = blurh(img, 9)
# cv2.imwrite('03 - blurh.png', img_output*255)

img_output = chadBlur(img, 9)
cv2.imwrite('04 - chadblur.png', img_output*255)
cv2.imshow('ChadBlur', img_output*255)
