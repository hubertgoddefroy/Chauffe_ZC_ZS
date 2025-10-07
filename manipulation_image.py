import os
import glob
import datetime


def renommer_image_plus_recente(dossier, addition_nom, prefixe='image_', extension='*.tif'):
    # Obtenir la liste de toutes les images dans le dossier
    liste_images = glob.glob(os.path.join(dossier, extension))

    if not liste_images:
        print("Aucune image trouvée dans le dossier.")
        return

    # Trouver l'image la plus récente en fonction de la date de modification
    image_plus_recente = max(liste_images, key=os.path.getmtime)
    date_modification = datetime.datetime.fromtimestamp(os.path.getmtime(image_plus_recente))

    # Extraire le chemin, le nom et l'extension de l'image
    chemin, ancien_nom_complet = os.path.split(image_plus_recente)
    nom, extension = os.path.splitext(ancien_nom_complet)

    # Créer le nouveau nom de fichier
    nouveau_nom = f"{nom}_{str(addition_nom)}{extension}"
    nouveau_chemin = os.path.join(chemin, nouveau_nom)

    # Renommer l'image
    os.rename(image_plus_recente, nouveau_chemin)


def obtenir_chemin_image_plus_recente_motif(dossier, motif, extension):
    motif_complet = f"{dossier}\\{motif}*{extension}"
    fichiers = glob.glob(motif_complet)
    if not fichiers:
        print("Aucune image récente correspondante trouvée")
    else:
        fichier_recent = max(fichiers, key=os.path.getmtime)
        return fichier_recent