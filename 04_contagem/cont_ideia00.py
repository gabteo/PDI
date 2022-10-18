import sys
import numpy as np
import cv2

INPUT_IMAGE = '205.bmp'

def binLateralGauss(imgGray):
    imgBlur = cv2.GaussianBlur(imgGray, (25, 25), 4)
    #cv2.imshow('gaussBlur', imgBlur)

    imgBlurBilat = cv2.bilateralFilter(imgGray,11,45,45)
    #cv2.imshow('Bilateral', imgBlurBilat)

    imgGaussBilat = cv2.GaussianBlur(imgBlurBilat, (25, 25), 4)
    blurBilatGauss = (imgBlur-imgGaussBilat)*50
    return blurBilatGauss

def main():

    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print('Cannot open image')
        sys.exit()
    cv2.imshow('Imagem original', img)
    img = np.float32(img) / 255
    imgBackground = np.copy(img)

    # ESCALA DE CINZA ------------------------------
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Escala de cinza', imgGray)
    #-----------------------------------------------

    blurBilatGauss = binLateralGauss(imgGray)
    cv2.imshow('blur Bilat Gauss', blurBilatGauss)
    x, imgBin = cv2.threshold(blurBilatGauss, .5, 1, cv2.THRESH_BINARY)
    cv2.imshow('binarizada', imgBin)
    

    # otsu
    imgGaussBlur = cv2.GaussianBlur(imgGray, (25, 25), 4)
    ret3,otsu = cv2.threshold(imgGaussBlur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('otsu', otsu)


    """ imgMediana = cv2.medianBlur(imgBlur, 5)
    cv2.imshow('mediana', imgMediana) """
    
    #adaptativeThresh = cv2.adaptiveThreshold(imgGray*255,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #cv2.imshow('binarizada adapt', adaptativeThresh)
    
    
    
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()