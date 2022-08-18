# Exemplo: manipulando imagens com OpenCV (versão Python).

import timeit
import cv2
import numpy as np

IN_IMG = 'teste.jpg'

# Abrindo a imagem. A imagem é armazenada em um array numpy.
# A função imread carrega uma imagem de um arquivo. Ela tem um segundo
# parâmetro opcional que indica o número de canais da imagem. O valor default
# é cv2.IMREAD_COLOR, que lê as imagens com 3 canais. Se o parâmetro for mudado
# para cv2.IMREAD_GRAYSCALE, a imagem é carregada em escala de cinza. Cuidado: a
# ordem dos canais na imagem colorida é B-G-R!
img = cv2.imread (IN_IMG)
if img is None:
    print ('Erro abrindo %s' % IN_IMG)
rows, cols, channels = img.shape

# Convertendo para float32.
# Dependendo da sequência de operações, e recomendável fazer esta conversão.
# (mas nem sempre é necessario)
img = img.astype (np.float32) / 255

# Para exemplificar a forma de acesso aos dados da imagem, vamos criar uma
# versão em escala de cinza dela. A conta é:
#
# cinza = 0.299r + 0.587g + 0.114b
#
# Lembrando que a ordem dos canais na imagem colorida é (B, G, R).

# Faremos isso quatro vezes, para comparar o desempenho.
img_gs = np.empty ((rows, cols, 1), np.float32)

# Versão 1: percorrendo pixel a pixel. Esta operação é lenta, e deve ser evitada
# quando possivel.
start_time = timeit.default_timer ()
for row in range (rows):
    for col in range (cols):
        img_gs [row,col,0] = img [row,col,0]*0.114 + img [row,col,1]*0.587 + img [row,col,2]*0.299
print ('Tempo pixel a pixel: %f' % (timeit.default_timer () - start_time))

# Versão 2: acessando como um array numpy. Quando precisar percorrer a imagem,
# sempre tente encontrar uma forma de fazer assim.
start_time = timeit.default_timer ()
img_gs [:,:,0] = img [:,:,0]*0.114 + img [:,:,1]*0.587 + img [:,:,2]*0.299
print ('Tempo numpy: %f' % (timeit.default_timer () - start_time))

# Versão 3: usando a função embutida do OpenCV.
start_time = timeit.default_timer ()
img_gs = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
print ('Tempo OpenCV (sem buffer): %f' % (timeit.default_timer () - start_time))

# Versão 4: usando a função embutida do OpenCV, mas reaproveitando o buffer que
# já tínhamos alocado. Na maior parte dos casos, é a melhor alternativa.
start_time = timeit.default_timer ()
cv2.cvtColor (img, cv2.COLOR_BGR2GRAY, dst = img_gs)
print ('Tempo OpenCV (com buffer): %f' % (timeit.default_timer () - start_time))

# Salvando. Note que eu preciso multiplicar de novo por 255, mas não preciso
# reconverter para inteiro.
cv2.imwrite ('cinza.png', img_gs*255)

# Mostrando os resultados.
cv2.imshow ('cor', img)
cv2.imshow ('cinza', img_gs)

# A função waitKey fica esperando o usuário pressionar uma tecla. Ela recebe um
# parâmetro, com valor default 0, que diz quantos milissegundos a função
# espera - se o valor for menor ou igual a 0, a função espera indefinidamente.
# O valor de retorno é o código ASCII da tecla pressionada - neste caso, não
# importa. Experimente mudar o parâmetro para 1000 para ver o que acontece.
cv2.waitKey ()
cv2.destroyAllWindows ()
