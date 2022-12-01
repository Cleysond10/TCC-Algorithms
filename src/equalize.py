import os
from os import listdir
from matplotlib import pyplot as plt
import numpy as np
import cv2


def generate_histogram(path):
    """Function to plt the image histogram by opencv."""
    filename = os.path.basename(path).split('.')[0]
    image = cv2.imread(path)
    CHANNEL = [0]
    HIST_SIZE = [256]
    RANGE = [0, 255]
    histogram = cv2.calcHist(
        image, CHANNEL, None, HIST_SIZE, RANGE)
    plt.subplot(111), plt.plot(histogram)
    plt.savefig(f'{filename}_hist')
    plt.clf()


def opencv_equalize(path):
    """Function equalize image in YCrCb with openCV default method."""
    filename = os.path.basename(path).split('.')[0]

    jpgColor = cv2.imread(path)

    # cv2.imwrite(f'{filename}_original.JPG', jpgColor)

    jpgYCrCb = cv2.cvtColor(jpgColor, cv2.COLOR_BGR2YCrCb)
    jpgYCrCb[:, :, 0] = cv2.equalizeHist(jpgYCrCb[:, :, 0])
    result = cv2.cvtColor(jpgYCrCb, cv2.COLOR_YCrCb2BGR)

    cv2.imwrite(f'{filename}_opencv_equaliz.JPG', result)


def quantil_equalize(path):
    """Function to equalize image in YCrCb with percentil of 0,1."""
    filename = os.path.basename(path).split('.')[0]

    # Read image no formato BGR do OpenCV
    jpgColor = cv2.imread(path)

    # Salva a imagem original
    cv2.imwrite(f'{filename}_Original.JPG', jpgColor)

    # Converte BRG para YCrCb com o formato
    jpgYCrCb = cv2.cvtColor(jpgColor, cv2.COLOR_BGR2YCrCb)

    # Isola a imagem em nível de cinza - GRAY, para melhorar os limiares dela
    jpGray = jpgYCrCb[:, :, 0]  # Obtem a banda Y da imagem YCrCb

    # Quantil's Equalize method

    # Step 1 - Definição dos Percentis [minPercentil,maxPercentil]
    minPercentil = np.percentile(jpGray, 1)
    maxPercentil = np.percentile(jpGray, 99)

    # Step 2 - Truncamentodos dos dados pelos Percentis [minPercentil,maxPercentil]
    jpgTrunc = jpGray

    n_linhas = jpgTrunc.shape[0]

    for i in range(n_linhas):
        arr = jpgTrunc[i, :]
        jpgTrunc[i, np.where(arr > maxPercentil)] = maxPercentil
        jpgTrunc[i, np.where(arr < minPercentil)] = minPercentil

    # Step 3 - Mapeamento dos dados [minPercentil,maxPercentil] para [0,255]
    jpgMap = jpgTrunc

    n2_linhas = jpgMap.shape[0]

    razao = maxPercentil - minPercentil

    for i in range(n2_linhas):
        arr2 = jpgMap[i, :]
        jpgMap[i, :] = ((arr2 - minPercentil)/razao)*255

    # Altera o valor da banda Y na imagem YCrCb para converter para a BGR em seguida.
    jpgYCrCbResult = jpgYCrCb
    # Obtem a banda Y da imagem YCrCb Resultante
    jpgYCrCbResult[:, :, 0] = jpgMap
    jpgResult = cv2.cvtColor(jpgYCrCbResult, cv2.COLOR_YCrCb2BGR)

    # Salva a imagem final
    cv2.imwrite(f'{filename}_quantil_equaliz.JPG', jpgResult)


# # def quantil_equalize_YUV(path):
#     """Function to equalize image in YUV with percentil of 0,1."""
#     filename = os.path.basename(path).split('.')[0]

#     jpgColor = cv2.imread(path)
#     jpgYUV = cv2.cvtColor(jpgColor, cv2.COLOR_BGR2YUV)

#     jpGray = jpgYUV[:, :, 0]

#     minPercentil = np.quantile(jpGray, 0.001)
#     maxPercentil = np.quantile(jpGray, 0.999)

#     jpgTrunc = jpGray
#     n_linhas = jpgTrunc.shape[0]
#     for i in range(n_linhas):
#         arr = jpgTrunc[i, :]
#         jpgTrunc[i, np.where(arr > maxPercentil)] = maxPercentil
#         jpgTrunc[i, np.where(arr < minPercentil)] = minPercentil

#     jpgMap = jpgTrunc
#     n2_linhas = jpgMap.shape[0]
#     razao = maxPercentil - minPercentil
#     for i in range(n2_linhas):
#         arr2 = jpgMap[i, :]
#         jpgMap[i, :] = ((arr2 - minPercentil)/razao)*255

#     jpgYUVResult = jpgYUV
#     jpgYUVResult[:, :, 0] = jpgMap
#     jpgResult = cv2.cvtColor(jpgYUVResult, cv2.COLOR_YUV2BGR)

#     cv2.imwrite(f'{filename}_YUV.JPG', jpgResult)


DIRECTORY = "C:/Users/CLEYSON/Documents/TCC/tcc_program/teste"

for file in listdir(DIRECTORY):
    if (file.endswith(".JPEG") or file.endswith(".JPG")
            or file.endswith(".jpeg") or file.endswith(".jpg")):
        photo_path = DIRECTORY + '/' + file
        generate_histogram(photo_path)
