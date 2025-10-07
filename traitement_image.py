import tifffile
import numpy as np


def obtenir_intensite(mw, mh, chemin_image):
    image_array = tifffile.imread(chemin_image)
    taille_image = np.shape(image_array)
    roi = image_array[int((mh / 100) * taille_image[0]):int((1 - (mh / 100)) * taille_image[0]),
          int((mw / 100) * taille_image[1]):int((1 - (mw / 100)) * taille_image[1])]

    # Calcul de l'histogramme
    hist, bin_edges = np.histogram(roi, bins=4096, range=(0, 4095))

    # Trouver l'indice du bin avec le maximum de pixels
    max_bin_index = np.argmax(hist)

    # L'abscisse du maximum
    abscisse_max = bin_edges[max_bin_index]

    # print("Abscisse du maximum de l'histogramme :", abscisse_max)
    return abscisse_max


def obtenir_temperature(chemin_image):
    init = chemin_image.index("(")
    fin = chemin_image.index(")")
    temperature = 1001
    # print(init)
    # print(fin)
    # print(fin - init)
    if fin - init == 3:
        temperature = int(chemin_image[init + 1:fin])
    else:
        print("mauvaise lecture de la température (paranthèse dans les chemins d'accès ?")
    return temperature