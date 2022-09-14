import sys
import timeit
import numpy as np
import cv2

INPUT_IMAGE =  'tree.jpg'

def blurIngenuo(img, fullw):
    w = fullw//2
    img_return = np.array
    img_return = img.reshape((img.shape[0], img.shape[1], 1))

    for y in range(w, len(img)-w):
        for x in range(w, len(img[0])-w):
            # para cada pixel
            soma = 0
            for i in range(-w, w+1):
                for j in range(-w, w+1):
                    # soma cada pixel da janela
                    soma += img[y+i, x+j]
            media = soma / fullw**2
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

def blurIntegral(img, halfWidth):
    pass



def main ():
    ingenuo = 1
    separavel = 2
    integral = 3
    algoritmo = ingenuo

    # Leitura do arquivo-----------------------------------
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print('Cannot open image')
        sys.exit()

    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255

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
        img_output = blurIntegral(img, 9)
        cv2.imwrite('04 - blurIntegral.png', img_output*255)
        print ('Tempo integral: %f' % (timeit.default_timer () - start_time))

    # mostrar a imagem de saída
    cv2.imshow('Output', img_output*255)    # TODO saída branca
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
