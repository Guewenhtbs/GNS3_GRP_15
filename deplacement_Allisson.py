import os
import shutil

# Dictionnaire des correspondances entre numéro et UUID
correspondance_numero_dossier = {
    "1": "fb64a267-ad5f-42bc-bd53-184fa2bfb77b",
    "2": "e7f857cc-60ba-481f-bd6d-bf321d8a309f",
    "3": "a6ac3bbc-246d-41e8-844b-6ebab06a93ef",
    "4": "a72025c9-f22b-48c1-8c7c-dac53f474a0a",
    "5": "73c76311-ad91-4093-9ac7-120f7bf28246",
    "6": "1a303579-5ccd-49d8-955a-502f537015dd",
    "7": "3db499c3-0da1-4d59-80ab-7e2e9e2d7d8a",
    "8": "673017bf-52fb-46db-92d8-3954285db497",
    "9": "c8644c63-52fb-45e3-95f8-4922afe86cd0",
    "10": "90ac2d6b-9388-4476-8cc8-16f60f15378a",
    "11": "fe196024-d77f-4239-81d5-3c0cb82d15ce",
    "12": "9239cfe6-441c-446e-984e-1077e5dcabba"
}

# Chemin du dossier contenant les fichiers .cfg
chemin_dossier_source = 'C:/Users/pc/OneDrive/Documents/GNS3/GNS3_GRP_15/Config_bgp'  # Remplacez cela par votre chemin réel

# Chemin du dossier de destination principal
chemin_dossier_destination = 'C:/Users/pc/OneDrive/Documents/GNS3/GNS3_GRP_15/GNS3_file/project-files/dynamips'

for fichier in os.listdir(chemin_dossier_source):
    numero = fichier[1:fichier.find('_')] 
    dossier_correspondant = correspondance_numero_dossier[numero]
    chemin_dossier_correspondant = os.path.join(chemin_dossier_destination, dossier_correspondant, 'configs', fichier)
    shutil.move(os.path.join(chemin_dossier_source, fichier), chemin_dossier_correspondant)
