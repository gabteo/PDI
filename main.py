#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.8
ALTURA_MIN = 1
LARGURA_MIN = 1
N_PIXELS_MIN = 1

#===============================================================================

def binariza (img, threshold):

    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''
    rows, cols, channels = img.shape
    for row in range (rows):
        for col in range (cols):
            if (img [row,col] < THRESHOLD):
                img[row, col] = 0
            else:
                img[row, col] = 1

    #img = np.where(img < THRESHOLD, 0, 0)
    return img
    # TODO: escreva o código desta função.
    # Dica/desafio: usando a função np.where, dá para fazer a binarização muito
    # rapidamente, e com apenas uma linha de código!

#-------------------------------------------------------------------------------
def flood (label, labelMatrix, x0, y0, n_pixels):
    labelMatrix[x0,y0] = label

    n_pixels += 1
    n = 0
    temp = {
        'T': y0,
        'L': x0,
        'B': y0+15,
        'R': x0+15,
        'n_pixels': 0
    }

    info = {
        'T': temp['T'],
        'L': temp['L'],
        'B': temp['B'],
        'R': temp['R'],
        'n_pixels': n_pixels + n
    }

    if (labelMatrix[x0,y0+1] == -1):
        temp = flood(label, labelMatrix, x0,y0+1, n_pixels)
        if (temp['T'] < info['T']):
            info['T'] = temp['T']
        if (temp['B'] > info['B']):
            info['B'] = temp['B']
        if (temp['L'] < info['L']):
            info['L'] = temp['L']
        if (temp['R'] > info['R']):
            info['R'] = temp['R']
        n += temp['n_pixels']

    if (labelMatrix[x0+1,y0] == -1):
        temp = flood(label, labelMatrix, x0+1,y0, n_pixels)
        if (temp['T'] < info['T']):
            info['T'] = temp['T']
        if (temp['B'] > info['B']):
            info['B'] = temp['B']
        if (temp['L'] < info['L']):
            info['L'] = temp['L']
        if (temp['R'] > info['R']):
            info['R'] = temp['R']
        n += temp['n_pixels']

    if (labelMatrix[x0-1, y0] == -1):
        temp = flood(label, labelMatrix, x0-1, y0, n_pixels)
        if (temp['T'] < info['T']):
            info['T'] = temp['T']
        if (temp['B'] > info['B']):
            info['B'] = temp['B']
        if (temp['L'] < info['L']):
            info['L'] = temp['L']
        if (temp['R'] > info['R']):
            info['R'] = temp['R']
        n += temp['n_pixels']

    if (labelMatrix[x0, y0-1] == -1):
        temp = flood(label, labelMatrix, x0, y0-1, n_pixels)
        if (temp['T'] < info['T']):
            info['T'] = temp['T']
        if (temp['B'] > info['B']):
            info['B'] = temp['B']
        if (temp['L'] < info['L']):
            info['L'] = temp['L']
        if (temp['R'] > info['R']):
            info['R'] = temp['R']
        n += temp['n_pixels']



    '''yMin = y0
    xMin = x0
    yMax = y0
    xMax = x0'''
    info['n_pixels'] = n_pixels + n

    '''info = {
        'T': temp['T'],
        'L': temp['L'],
        'B': temp['B'],
        'R': temp['R'],
        'n_pixels': n_pixels + n
    }'''
    return info

#-------------------------------------------------------------------------------

def rotula (img, largura_min, altura_min, n_pixels_min):
    rows, cols, channels = img.shape

    labelMatrix = np.empty((rows, cols))
    outputList = []

    for row in range(rows):
        for col in range(cols):
            if (img[row, col] == 0):
                labelMatrix[row, col] = 0
            else:
                labelMatrix[row, col] = -1

    label = 1
    for row in range(rows):
        for col in range(cols):
            if (labelMatrix[row, col] == -1):
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
                if (component['n_pixels'] > 10):
                    outputList.append(component)
                    label += 1
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    '''n_pixels = 50
    t= 50
    l= 50
    b= 50
    r= 50'''

    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.

    return outputList
#===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza (img, THRESHOLD)
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
