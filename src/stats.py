from os import listdir
from scipy import stats
import numpy as np
import cv2

DIRECTORY = "C:/Users/CLEYSON/Desktop/TCC/Banco_De_Imagens-TCC/Claras"

f = open("Claras-Stats.txt", "w+", encoding="utf8")


def get_image_stats(jpg):
    """Function getting image stats."""
    mean = np.mean(jpg, axis=None)
    mean_result = format(mean, '.2f')
    f.write(f' MÉDIA:{mean_result}')

    median = np.median(jpg, axis=None)
    f.write(f' MEDIANA:{median}')

    mode = stats.mode(jpg, axis=None, keepdims=False).mode
    f.write(f' MODA:{mode}')

    if mean == median == mode:
        f.write(' CONCLUSÃO:NORMAL')
    elif mean > median > mode:
        f.write(' CONCLUSÃO:ESCURA')
    elif mean < median < mode:
        f.write(' CONCLUSÃO:CLARA')
    else:
        f.write(' CONCLUSÃO:??')


for file in listdir(DIRECTORY):
    if (file.endswith(".JPEG") or file.endswith(".JPG")
            or file.endswith(".jpeg") or file.endswith(".jpg")):
        f.write('\r\n Arquivo:')
        f.write(file)
        filename = DIRECTORY + '/' + file
        image = cv2.imread(filename, 0)
        get_image_stats(image)

f.close()
