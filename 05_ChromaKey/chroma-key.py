
from math import exp
import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

INPUT_IMAGE = 'img_in\GSPlate.0116.bmp'
#INPUT_IMAGE = 'img_in\hcw_godiva_medium.0110.png'
#INPUT_IMAGE = 'img_in\green255.png'
#INPUT_IMAGE = 'img_in\greenScale.png'
BACKGROUND = 'bg\embassy_shootout2.0116.bmp'


H = 0
L = 1
S = 2
""" 
GREEN_MAX = 73
GREEN_MIN = 37 """
GREEN_MAX = 160
GREEN_MIN = 75

LUMA_MAX = 255*0.95
LUMA_MIN = 255*0.05

SATURATION_MAX = 255*1
SATURATION_MIN = 255*0.1

# site com vários exemplos de chroma key para praticar:
# https://www.hollywoodcamerawork.com/green-screen-plates.html

def normalizar(valor, max, min):
    return (valor-min)/(max-min)

def main():
    hist = True
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    bg = cv2.imread(BACKGROUND, cv2.IMREAD_COLOR)
    # imgTeste = cv2.cvtColor(imgTeste, cv2.COLOR_BGR2GRAY)
    rows, cols, lixo = img.shape

    cv2.imshow('input', img)
    cv2.imshow('backgroung', bg)

    # converter pra HSL
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    # H está no range [0,180???]. L e S em [0,255]
    # ATENÇÃO: HLS, não HSL

    # hue do primeiro pixel: hls[0, 0, 0]
    # hls[linha, coluna, HLS]
    #print(hls[:, :, H])

    # imprime histograma do hue:
    if hist:
        figure, axis = plt.subplots(3, 1)
        figure.set_label('Histograms')

        axis[0].hist((hls[:,:,H]).ravel(),180,[0,180])
        axis[0].set_title('Hue histogram')

        axis[1].hist((hls[:,:,L]).ravel(),255,[0,255])
        axis[1].set_title('Luma histogram')

        axis[2].hist((hls[:,:,S]).ravel(),255,[0,255])
        axis[2].set_title('Saturation histogram')

        plt.tight_layout()

    
    # R = 0, G = 255 e B = 0 resulta em H = 60
    alphaLayerColor = np.copy(hls)

    # loop para encontrar o verde da imagem (assume-se que há verde)
    huesVerdes = []
    nVerdes = 0
    for row in range(rows):
        for col in range(cols):
            if (hls[row, col, L] >= LUMA_MIN and hls[row, col, L] <= LUMA_MAX):
                # se não for muito claro ou muito escuro...
                if (hls[row, col, S] >= SATURATION_MIN and hls[row, col, S] <= SATURATION_MAX):
                    # se saturação não for muito fraca..

                    # calcula a média dos verdes, pra encontrar o verde "central"
                    if (hls[row, col, H] >= GREEN_MIN and hls[row, col, H] <= GREEN_MAX):
                        huesVerdes.append(hls[row, col, H])
                        nVerdes += 1
    
    mediaVerdes = np.mean(huesVerdes)
    # encontramos o verde "predominante"!

    # agora, buscamos uma gaussiana de hues
                    


    # mesmo loop, agora para calcular a camada alpha
    for row in range(rows):
        for col in range(cols):
            if (hls[row, col, L] >= LUMA_MIN and hls[row, col, L] <= LUMA_MAX):
                # se não for muito claro ou muito escuro...
                if (hls[row, col, S] >= SATURATION_MIN and hls[row, col, S] <= SATURATION_MAX):
                    # se saturação não for muito fraca..
                    if (hls[row, col, H] >= GREEN_MIN and hls[row, col, H] <= GREEN_MAX):
                        # se for verde...
                        
                        # a saturação tem um peso sigmoidal na determinação do valor do px
                        # TODO conferir fórmula
                        saturacao = normalizar(hls[row, col, S], 255, 0)
                        weightSat = 1/(1+exp(-saturacao))
                        #print(weightSat)

                        # TODO encontrar peso pro hue. Gaussiano?
                        weightHue

                        # peso final 
                        peso = weightSat*weightHue
                    
                else:
                    # se tiver certeza que não tem verde, mantém px original
                    alphaLayerColor[row, col, L] = 255
            else:
                # se tiver certeza que não tem verde, mantém px original
                alphaLayerColor[row, col, L] = 255
    
    alphaLayerColor = cv2.cvtColor(alphaLayerColor, cv2.COLOR_HLS2BGR)
    alphaLayer = cv2.cvtColor(alphaLayerColor, cv2.COLOR_BGR2GRAY)

    cv2.imshow("alpha", alphaLayer)
    cv2.imshow("alphaColro", alphaLayerColor)

    """     for px in hls[:, :, :]:
        print(px)
        if (px[H] == 54):
           print("hi",px) """


    # converter pra HSL
    # calcular valores HSL de interesse

    # balanço de branco automático? como detectar o verde mais presente?
    # ideia 1:
    # fazer um "histograma de verdes": o verde com mais presença é o verde desejado

    # ideia 2:
    # histograma de hue. Na faixa esperada pro verde, encontrar média/mediana/moda (escolher o melhor??)
    # "centralizar o verde nesse valor"

    # zerar luminância dos valores de interesse
    # converter a img com luma zerado pra BW
    # exibir alpha layer
    # cv2 addweighted, mas o peso é a alpha layer
    plt.show()
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()