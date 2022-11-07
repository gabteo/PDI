# from math import sqrt
import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

INPUT_IMAGE = 'img_in\GSPlate.0116.bmp'
BACKGROUND = 'bg\embassy_shootout2.0116.bmp'

# site com vários exemplos de chroma key para praticar:
# https://www.hollywoodcamerawork.com/green-screen-plates.html

def main():

    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    bg = cv2.imread(BACKGROUND, cv2.IMREAD_COLOR)

    cv2.imshow('input', img)
    cv2.imshow('backgroung', bg)

    hsl = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    # H está no range [0,180???]. L e S em [0,255]



    # 
    # imgTeste = cv2.cvtColor(imgTeste, cv2.COLOR_BGR2GRAY)


    # balanço de branco automático? como detectar o verde mais presente?
    # fazer um "histograma de verdes": o verde com mais presença é o verde desejado
    # converter pra HSL
    # calcular valores HSL de interesse
    # zerar luminância dos valores de interesse
    # converter a img com luma zerado pra BW
    # exibir alpha layer
    # cv2 addweighted, mas o peso é a alpha layer
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()