import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

np.set_printoptions(threshold=sys.maxsize)

INPUT_IMAGE = '150.bmp'

pxBlob = -1

def flood (label, labelMatrix, y0, x0, n_pixels):
    global pxBlob
    #print('flood')
    labelMatrix[y0,x0] = label
    rows, cols = labelMatrix.shape
    pxBlob += 1
    n_pixels += 1
    n = 0
    # armazenamento temporário da saída de flood (chamada recursiva) para comparação com info (abaixo)
    temp = {
        'T': y0,
        'L': x0,
        'B': y0,
        'R': x0,
        'n_pixels': 0
    }


    # output da função flood
    info = {
        'T': temp['T'],
        'L': temp['L'],
        'B': temp['B'],
        'R': temp['R'],
        'n_pixels': n_pixels
    }

    # vetores de vizinhos para iteração, cuidando das bordas da imagem
    n0 = labelMatrix[y0+1, x0] #if (y0+1) < rows else 0
    n1 = labelMatrix[y0, x0+1] #if (x0+1) < cols else 0
    n2 = labelMatrix[y0, x0-1] #if (x0-1) >= 0 else 0
    n3 = labelMatrix[y0-1, x0] #if (y0-1) >= 0 else 0

    neighbors = [n0, n1, n2, n3]
    neighborsIndex = [[y0+1, x0], [y0, x0+1], [y0, x0-1], [y0-1, x0]] 

    # para cada vizinho...
    for index in range(len(neighbors)):
            
        # check for image bounds
        # if ((index == 0 and (y0+1) < rows) or (index == 1 and (x0+1) < cols) or (index == 2 and (x0-1) >= 0) or (index == 3 and (y0-1) >= 0)):
            # se o vizinho é de interesse e não foi visitado...
        if (neighbors[index] == -1):
            # flood fill no vizinho
            # print(n)
            # print(labelMatrix)
            temp = flood(label, labelMatrix, neighborsIndex[index][0], neighborsIndex[index][1], n_pixels)
            #print(temp)
        # verifica se as bordas aumentaram
        if (temp['T'] < info['T']):
            info['T'] = temp['T']
        if (temp['B'] > info['B']):
            info['B'] = temp['B']
        if (temp['L'] < info['L']):
            info['L'] = temp['L']
        if (temp['R'] > info['R']):
            info['R'] = temp['R']
        # soma os pixels de temp à saída atual de flood
        n += temp['n_pixels']

    info['n_pixels'] = n_pixels + n
    # print(info['n_pixels'])
    return info

#-------------------------------------------------------------------------------

def rotula (img, largura_min=0, altura_min=0, n_pixels_min=0):
    
    global pxBlob

    rows, cols = img.shape

    labelMatrix = np.empty((rows, cols))
    outputList = []
    sizeList = []

    # Rotula os pixels de interesse como não percorridos
    for row in range(rows):
        for col in range(cols):
            if (img[row, col] == 0):
                labelMatrix[row, col] = 0
            else:
                labelMatrix[row, col] = -1
    # print(labelMatrix)
    # recursão
    sys.setrecursionlimit(5000)
    label = 1
    # para cada pixel...
    for row in range(rows):
        for col in range(cols):
            # flood fill no pixel, se é de interesse e não visitado
            if (labelMatrix[row, col] == -1):
                pxBlob = -1
                n_pixels = 0
                info = flood(label, labelMatrix, row, col, n_pixels)
                component = {
                    "label": label,
                    "n_pixels": info['n_pixels'],
                    'T': info['T'],
                    'L': info['L'],
                    'B': info['B'],
                    'R': info['R']
                }
                # print(component['n_pixels'])
                # verifica se componente tem as dimensões mínimas e adiciona à saída de rotula
                if (component['n_pixels'] > n_pixels_min):
                    outputList.append(component)
                    label += 1
                    sizeList.append(pxBlob)

    return outputList, sizeList


def main():
    hist = 0
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    imgTeste = cv2.imread("n1px.bmp", cv2.IMREAD_COLOR)
    imgTeste = cv2.cvtColor(imgTeste, cv2.COLOR_BGR2GRAY)

    img1px = np.zeros((50, 50))
    img1px[20, 20], img1px[20, 21], img1px[21, 20], img1px[21, 21] = 255, 255, 255, 255
    img1px = img1px.astype(np.float32)
    #print(img1px)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img255 = np.copy(imgGray)
    imgFloat = imgGray.astype(np.float32) / 255
    # print(img)
    cv2.imshow('IMG', imgFloat)

    imgBlur = cv2.medianBlur(img255, 7)

    imgCanny = cv2.Canny(imgBlur, 100, 110)
    cv2.imshow('Canny', imgCanny)

    #hist = cv2.calcHist([img255],[0],None,[256],[0,256])
    img_median = cv2.medianBlur(imgFloat, 5)
    img_median = cv2.medianBlur(img_median, 5)
    cv2.imshow('median twice', img_median)

    img_gaussian = cv2.GaussianBlur(img_median, (201, 201), 0)
    blobs = img_median - img_gaussian
    blobs = np.where(blobs < 0, 0, blobs)
    cv2.imshow('Blobs', blobs)
    cv2.imshow('Gaussian', img_gaussian)

    ret2,otsu = cv2.threshold((blobs * 255).astype(np.uint8),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('otsu', otsu)

    kernel = np.ones((3, 3))

    erosion = cv2.erode(otsu, kernel, iterations=1)
    closing = cv2.dilate(erosion, kernel, iterations=1)
    cv2.imshow('closing', closing)

    components, sizeList = rotula(closing)
    #print(components)
    print(sizeList)
    plt.boxplot(sizeList)
    fig1, ax1 = plt.subplots()
    ax1.set_title('Basic Plot')
    plt.boxplot(sizeList)
    plt.show()

    """  for blob in components:
        print(blob['n_pixels']) """
    for c in components:
        cv2.rectangle (img, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,255))
    
   

    cv2.imshow('Rect', img)
    
    if hist:
        plt.figure("Original")
        plt.hist((imgFloat*255).ravel(),255,[0,255])
        plt.figure("Blobs")
        plt.hist((blobs * 255).ravel(),255,[0,255])
        plt.figure("Median")
        plt.hist((img_median * 255).ravel(),255,[0,255])
        plt.show()

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()