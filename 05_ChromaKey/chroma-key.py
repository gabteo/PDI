
from math import exp
import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

INPUT_IMAGE = 'img_in\\8.bmp'
#INPUT_IMAGE = 'img_in\GSPlate.0116.bmp'

#INPUT_IMAGE = 'img_in\hcw_godiva_medium.0110.png'
#INPUT_IMAGE = 'img_in\green255.png'
#INPUT_IMAGE = 'img_in\greenScale.png'
BACKGROUND = 'bg\minecraft_bg.jpg'


H = 0
L = 1
S = 2

GREEN_MAX = 55+13
GREEN_MIN = 55-13

LUMA_MAX = 255*0.8
LUMA_MIN = 255*0.15

SATURATION_MAX = 255*1
SATURATION_MIN = 255*0.25

# site com vários exemplos de chroma key para praticar:
# https://www.hollywoodcamerawork.com/green-screen-plates.html

def normalizar(valor, max, min = 0):
    return (valor-min)/(max-min)

def main():
    hist = False
    bgColor = False #define se background é cor sólida
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    bg = cv2.imread(BACKGROUND, cv2.IMREAD_COLOR)
    
    rows, cols, _ = img.shape
    dim = (cols, rows)
  
    # resize image
    bg = cv2.resize(bg, dim, interpolation = cv2.INTER_AREA)


    alphaLayer = np.copy(img)
    alphaLayer = cv2.cvtColor(alphaLayer, cv2.COLOR_BGR2GRAY)
    alphaLayer = alphaLayer.astype(np.float32)/255

    cv2.imshow('input', img)

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
    #alphaLayerColor = np.copy(hls)

    # loop para encontrar o verde da imagem (assume-se que há verde)
    """     huesVerdes = []
    saturacoesVerdes = []
    lumasVerdes = []
    distVerdes = []
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
                        saturacoesVerdes.append(hls[row, col, S])
                        lumasVerdes.append(hls[row, col, L])
                        nVerdes += 1

    mediaHuesVerdes = np.mean(huesVerdes)
    mediaLumasVerdes = np.mean(lumasVerdes)

    mediaSaturacoesVerdes = np.mean(saturacoesVerdes)
    # encontramos o verde "predominante"! Temos o HSL dele
    mediaVerdes = (mediaHuesVerdes, mediaLumasVerdes, mediaSaturacoesVerdes) """
    
    """ for i in range(nVerdes):
        hueDist = abs(huesVerdes[i] - mediaHuesVerdes)
        distVerdes.append(hueDist)

    # agora, buscamos uma gaussiana de hues
    distVerdesNormalizadas = []
    for i in range(nVerdes):
        distMax = max(abs(GREEN_MAX-mediaHuesVerdes), abs(GREEN_MIN-mediaHuesVerdes))
        distVerdesNormalizadas.append(normalizar(distVerdes[i], distMax, 0)) """


    # mesmo loop, agora para calcular a camada alpha
    for row in range(rows):
        for col in range(cols):
            if (hls[row, col, H] >= GREEN_MIN and hls[row, col, H] <= GREEN_MAX):
                # se for verde...
                if (hls[row, col, L] >= LUMA_MIN and hls[row, col, L] <= LUMA_MAX):
                    # se não for muito claro ou muito escuro...
                    if (hls[row, col, S] >= SATURATION_MIN and hls[row, col, S] <= SATURATION_MAX):
                        # se saturação não for muito fraca...
                            if (hls[row, col, L] < (LUMA_MIN*1.5) and hls[row, col, S] < SATURATION_MIN*1.2):
                                alphaLayer[row, col] = 1
                                hls[row, col, S] = 0
                                pass
                            else:
                                # a saturação tem um peso sigmoidal na determinação do valor do px
                                saturacao = normalizar(hls[row, col, S], 255, 0)
                                weightSat = 1/(1+exp(5*(-saturacao+0.5)))
                                
                                luminancia = normalizar(hls[row, col, L], 255, 0)
                                pesoLuma = abs(luminancia - 0.5)

                                # peso final 
                                peso = weightSat * pesoLuma

                                alphaLayer[row, col] = peso
                    else:
                        alphaLayer[row, col] = 1
                        hls[row, col, S] = 0
                else:
                    alphaLayer[row, col] = 1
                    hls[row, col, S] = 0
            elif(hls[row, col, H] >= GREEN_MIN-10 and hls[row, col, H] <= GREEN_MAX+10):
                hls[row, col, S] = hls[row, col, S]*0.5
                alphaLayer[row, col] = 1
            else:
                # se tiver certeza que não tem verde, mantém px original
                alphaLayer[row, col] = 1
    
    alphaBinary = np.copy(alphaLayer)
    _, alphaBinary = cv2.threshold(alphaBinary, 0.95, 1, cv2.THRESH_BINARY)
    cv2.imshow("alpha binary", alphaBinary)

    # kernel = np.ones((3,3))
    # alphaBinary = cv2.dilate(alphaBinary, kernel, iterations=1)
    # alphaBinary = cv2.erode(alphaBinary, kernel, iterations=1)

    # for row in range(rows):
    #     for col in range(cols):
    #         if (alphaBinary[row, col] == 1):
    #             alphaLayer[row, col] = 1

    for row in range(rows):
        for col in range(cols):
            if(alphaLayer[row, col] < 1):
                hls[row, col, S] = 0

    alphaLayer = np.where(np.logical_and(alphaLayer <= 0.4, alphaLayer > 0.1), alphaLayer + 0.2, alphaLayer)

    cv2.imshow("alpha", alphaLayer)

    alphaLayer = cv2.cvtColor(alphaLayer, cv2.COLOR_GRAY2BGR)
    alphaLayer = cv2.GaussianBlur(alphaLayer, (0,0), 1.5)
    alphaLayer = cv2.medianBlur(alphaLayer, 3)

    cv2.imshow("alpha blur", alphaLayer)

    if(bgColor == True):
        bg = np.copy(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        bg = cv2.cvtColor(bg, cv2.COLOR_GRAY2BGR)
        bg[:]=(235, 52, 82)

    dst = np.copy(img)
    img = cv2.cvtColor(hls, cv2.COLOR_HLS2BGR)

    for row in range(rows):
        for col in range(cols):
            dst[row, col] = img[row, col] * alphaLayer[row, col] + bg[row, col] * (1 - alphaLayer[row, col])

    cv2.imshow("final", dst)

    plt.show()
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()