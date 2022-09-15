import sys
import timeit
import numpy as np
import cv2

INPUT_IMAGE =  'tree.jpg'

def blurIngenuo(img, fullw):
    w = fullw//2
    img_return = np.array
    img_return = img.reshape((img.shape[0], img.shape[1], 3))

    for y in range(w, len(img)-w):
        for x in range(w, len(img[0])-w):
            # para cada pixel
            soma = 0
            for i in range(-w, w+1):
                for j in range(-w, w+1):
                    # soma cada pixel da janela
                    soma += img[y+i, x+j]
            media = soma / (fullw**2)
            img_return[y, x] = media

    return img_return

def chadBlur(img, fullw):
    w = fullw//2

    #img_return = np.array
    img_return = np.copy (img)
    print (img_return.dtype)
    #img_return = img.reshape((img.shape[0], img.shape[1], 1))

    for y in range(w, len(img)-w):
        soma = 0
        for x in range(w, len(img[0])-w):
            if (x == w):                
                for i in range(-w, w+1):
                    for j in range(-w, w+1):
                        soma += img[y+i, w+j]
            else:
                for k in range(-w, w+1):
                    soma += img[y+k, x+w]
                    soma -= img[y+k, x-w-1]
            media = soma / (fullw**2)
            img_return[y, x] = media

    return img_return

def blurSeparavel(img, halfWidth):
    pass

def blurIntegral(img, fullW):
    halfW = fullW // 2
    # fullW = 2*halfW+1
    img_return = np.copy (img)
    img_integral = np.array
    img_integral = img.reshape((img.shape[0], img.shape[1], 3))

    # criação da imagem integral --------------------------------
    # para cada linha y
    for y in range(0, len(img)):
        # primeiro px da linha é igual o original
        img_integral[y, 0] = img[y, 0]
        # para cada coluna fora a primeira
        for x in range(1, len(img[0])):
            # pixel é px original mais integral à esquerda
            img_integral[y, x] = img[y, x] + img_integral[y, x-1]


    # para cada linha y fora a primeira
    for y in range(1, len(img)):
        # para cada coluna x
        for x in range(0, len(img[0])):
            # pixel é igual a ele mais pixel de cima
            img_integral[y, x] += img_integral[y-1, x]
    # print(img_integral)

    # Obtenção da média ------------------------------------------
    # para cada pixel...
    for y in range(0, len(img)-halfW):
        for x in range(0, len(img[0])-halfW):
            # para cada pixel, janela:
            soma = 0
            soma += img_integral[y+halfW, x+halfW]
            winW = fullW
            winH = fullW
            if (y>halfW):
                soma -= img_integral[y-halfW-1, x+halfW]
            if (x>halfW):
                soma -= img_integral[y+halfW, x-halfW-1] 
            if (x>halfW and y>halfW):
                soma += img_integral[y-halfW-1, x-halfW-1]
            """ soma = img_integral[y+halfW, x+halfW] - img_integral[y-halfW-1, x+halfW] - img_integral[y+halfW, x-halfW-1] + img_integral[y-halfW-1, x-halfW-1]
            media = soma / (fullW**2)
            #print(media)
            img_return[y, x] = media """
            media = soma / (winH*winW)
            img_return[y, x] = media
    
    for y in range(0, halfW+1):
        break
        for x in range(0, len(img[0])-halfW):
            soma = 0
            soma += img_integral[y+halfW, x+halfW]
            winW = fullW
            winH = fullW
            #print(type(soma[0]))
            #print(img_integral[y+halfW, x-halfW-1][1])
            """ if not (y<=halfW):
                soma -= img_integral[y-halfW-1, x+halfW]
                winW = x + halfW  """
            if (x>halfW):
                soma -= img_integral[y+halfW, x-halfW-1] 
                winW = fullW
                #winH = y + halfW
                
            """  if not (y<=halfW):
                soma -= img_integral[y-halfW-1, x+halfW]
            if not (x<=halfW):
                soma -= img_integral[y+halfW, x-halfW-1] 
            if (x>=halfW and y>=halfW):
                soma += img_integral[y-halfW-1, x-halfW-1] """
                
            media = soma / (winH*winW)
            img_return[y, x] = media

    return img_return



def main ():
    ingenuo = 1
    separavel = 2
    integral = 3
    algoritmo = integral

    # Leitura do arquivo-----------------------------------
    # img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)

    if img is None:
        print('Cannot open image')
        sys.exit()

    img = img.reshape((img.shape[0], img.shape[1], 3))
    img = img.astype(np.float32)
    img /= 255

    # Algoritmos
    if algoritmo == ingenuo:
        start_time = timeit.default_timer ()
        img_output = blurIngenuo(img, 9)
        cv2.imwrite('04 - blurIngenuo.png', img_output*255)
        print ('Tempo ingênuo: %f' % (timeit.default_timer () - start_time))
    elif algoritmo == separavel:
        start_time = timeit.default_timer ()
        img_output = blurSeparavel(img, 9)
        cv2.imwrite('04 - blurSeparavel.png', img_output*255)
        print ('Tempo separável: %f' % (timeit.default_timer () - start_time))
    elif algoritmo == integral:
        start_time = timeit.default_timer ()
        img_output = blurIntegral(img, 55) 
        cv2.imwrite('04 - blurIntegral.png', img_output*255)
        print ('Tempo integral: %f' % (timeit.default_timer () - start_time))

    # mostrar a imagem de saída
    cv2.imshow('Output', img_output)    # TODO saída branca
    cv2.waitKey ()
    cv2.destroyAllWindows ()


    # print(type (img))
    # img_output = blurh(img, 9)
    # cv2.imwrite('03 - blurh.png', img_output*255)
    """ img_output = chadBlur(img, 9)
    cv2.imwrite('04 - chadblur.png', img_output*255)
    cv2.imshow('ChadBlur', img_output*255)
 """

if __name__ == '__main__':
    main ()
