import time
import subprocess
from manipulation_image import *
from traitement_image import *
from openpyxl import Workbook


def mesure_chauffe_ZC_snap(chemin_installation_ZS, chemin_dossier_enregistrement_image, nom_machine, puits, case_455,
                           case_730, case_455_730, nombre_iteration, frequence_enregistrement):
    process = subprocess.Popen(
        'cmd.exe',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='latin-1',  # ou 'cp850' pour la console Windows
        errors='replace',  # pour remplacer les caractères non décodables
        text=True,
        shell=True)

    process.stdin.write(
        chemin_installation_ZS + "/bin/ZymoCubeCtrl.exe " + chemin_installation_ZS + "/etc/ZymoCubeCtrl.ini" + '\n')
    process.stdin.flush()
    time.sleep(15)
    process.stdin.write(fr'reset AxHV_ZC_rfl_v1' + '\n')
    process.stdin.flush()
    for i in range(13):
        out = process.stdout.readline()
        print(out.strip())
    time.sleep(6)
    process.stdin.write(fr'start' + '\n')
    process.stdin.flush()
    for i in range(3):
        out = process.stdout.readline()
        print(out.strip())
    time.sleep(6)
    process.stdin.write(fr'goto ' + puits + '\n')
    process.stdin.flush()
    for i in range(4):
        out = process.stdout.readline()
        print(out.strip())
    time.sleep(7)

    ### Création fichier excel
    wb = Workbook()
    del wb["Sheet"]

    if case_455:
        onglet1 = wb.create_sheet(title="455")
    if case_730:
        onglet1 = wb.create_sheet(title="730")
    if case_455_730:
        onglet1 = wb.create_sheet(title="455")
        onglet2 = wb.create_sheet(title="730")

    for i_boucle in range(int(nombre_iteration)):

        ### Création d'un fichier excel intermédiaire tous les 100 itérations pour sécuriser l'export en cas de crach du PC
        if i_boucle % int(frequence_enregistrement) == 0:
            wb_temp = Workbook()
            del wb_temp["Sheet"]

            if case_455:
                onglet1_temp = wb_temp.create_sheet(title="455")
            if case_730:
                onglet1_temp = wb_temp.create_sheet(title="730")
            if case_455_730:
                onglet1_temp = wb_temp.create_sheet(title="455")
                onglet2_temp = wb_temp.create_sheet(title="730")

        ### Prise des clichés dans une ou deux longueurs d'onde
        if case_455 or case_455_730:
            process.stdin.write(fr'snap 455' + '\n')
            process.stdin.flush()
            for i in range(3):
                out = process.stdout.readline()
                print(out.strip())
            time.sleep(3)

        if case_730 or case_455_730:
            process.stdin.write(fr'snap 730' + '\n')
            process.stdin.flush()
            for i in range(3):
                out = process.stdout.readline()
                print(out.strip())
            time.sleep(3)

        ### Récupération de l'intensité représentative ainsi que de la température des clichés
        if case_455 or case_455_730:
            chemin_image_455 = obtenir_chemin_image_plus_recente_motif(chemin_dossier_enregistrement_image,
                                                                       puits + "_455", ".tif")
            temperature_image_455 = obtenir_temperature(chemin_image_455)
            intensite_image_455 = obtenir_intensite(25, 25, chemin_image_455)

        if case_730 or case_455_730:
            chemin_image_730 = obtenir_chemin_image_plus_recente_motif(chemin_dossier_enregistrement_image,
                                                                       puits + "_730", ".tif")
            temperature_image_730 = obtenir_temperature(chemin_image_730)
            intensite_image_730 = obtenir_intensite(25, 25, chemin_image_730)

        ### Suppression des clichés pour éviter la saturation du stockage
        if case_455 or case_455_730:
            os.remove(chemin_image_455)
        if case_730 or case_455_730:
            os.remove(chemin_image_730)

        ### Remplissage du fichier excel intermédiaire
        if case_455:
            onglet1_temp.append([f"{i_boucle}", f"{temperature_image_455}", f"{intensite_image_455}"])
        if case_730:
            onglet1_temp.append([f"{i_boucle}", f"{temperature_image_730}", f"{intensite_image_730}"])
        if case_455_730:
            onglet1_temp.append([f"{i_boucle}", f"{temperature_image_455}", f"{intensite_image_455}"])
            onglet2_temp.append([f"{i_boucle}", f"{temperature_image_730}", f"{intensite_image_730}"])

        ### Remplissage du fichier excel final
        if case_455:
            onglet1.append([f"{i_boucle}", f"{temperature_image_455}", f"{intensite_image_455}"])
        if case_730:
            onglet1.append([f"{i_boucle}", f"{temperature_image_730}", f"{intensite_image_730}"])
        if case_455_730:
            onglet1.append([f"{i_boucle}", f"{temperature_image_455}", f"{intensite_image_455}"])
            onglet2.append([f"{i_boucle}", f"{temperature_image_730}", f"{intensite_image_730}"])

        ### Enregistrement du fichier excel intermédiaire
        if (i_boucle + 1) % int(frequence_enregistrement) == 0:
            wb_temp.save(chemin_dossier_enregistrement_image + "\\mesure_chauffe_" + nom_machine + "_" + str(
                int((i_boucle + 1) / int(frequence_enregistrement))) + ".xlsx")

        ### Attente pour espacer les prises de cliché de 10 secondes
        if case_455_730:
            time.sleep(4)
        else:
            time.sleep(6.6)
        print(i_boucle + 1)

    ### Enregistrement du fichier excel
    wb.save(chemin_dossier_enregistrement_image + "\\mesure_chauffe_" + nom_machine + ".xlsx")

    process.stdin.write(fr'stop' + '\n')
    process.stdin.flush()
    print('STOPPED')
    time.sleep(10)
    process.stdin.write(fr'quit' + '\n')
    process.stdin.flush()
    time.sleep(3)
    print('EXITED')

    process.stdin.close()


def log_de_mesure(install_dir, save_dir, checkbox1_state, checkbox2_state, checkbox3_state, text_field_machine,
                  text_field_iteration, text_field_frequence, combo_box_selection):
    fichier_texte = save_dir + "/Calibration_" + text_field_machine + "_" + combo_box_selection + ".log"

    lignes = ["\n--- Données récupérées ---",
              "Dossier d'installation ZymoSoft : " + install_dir,
              "Dossier d'enregistrement des snap : " + save_dir,
              "455 ? " + str(checkbox1_state),
              "730 ? " + str(checkbox2_state),
              "455 & 730 ? " + str(checkbox3_state),
              "Nom Machine : " + text_field_machine,
              "Nombre d'intérations : " + text_field_iteration,
              "Période enregistrement : " + text_field_frequence,
              "Puits acquis : " + combo_box_selection,
              "--------------------------\n"]
    with open(fichier_texte, 'w', encoding='utf-8') as fichier:
        for ligne in lignes:
            fichier.write(ligne + "\n")