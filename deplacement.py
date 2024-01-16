import os
import shutil

# Dictionnaire des correspondances entre numéro et UUID
nom_fichier = {
    "1": "39a09daf-6bbb-49d2-bdef-bdece8410620",
    "2": "fe0ba0e8-6a04-4df7-9313-3e6fae359fa8",
    "3": "a1c19efa-228a-48e5-8a1d-823304341d74",
    "4": "75775339-44a9-4691-b549-9a79b4a4bfeb",
    "5": "e77dcbd6-4836-468f-a13e-a217f926ebe3",
    "6": "08ab2678-0b8c-4c30-8ed6-b98c4fdc7bb4",
    "7": "2e53cba6-d772-4921-9d10-3bb2434e917c",
    "8": "e832c8a7-6a47-445e-b387-e5131f76e1a7",
    "9": "15c3dfa8-cb83-4f97-b3cc-dc12aefd0783",
    "10": "852a964a-91e6-4e41-8fb2-4cbb3fc387c8",
    "11": "6228e624-4df2-4960-bc5e-18c4b13a3902",
    "12": "ee6eb131-eaa9-4247-a5c4-5e0522e20f51",
    "13": "92fd3895-4db0-4412-8d46-d2cc9be695db",
    "14": "acdcac23-67fc-40b3-9fbe-a495b49e42f5"
}

# Chemin du dossier contenant les fichiers .cfg
chemin_dossier_source = 'C:/Users/pc/OneDrive/Documents/GNS3/GNS3_GRP_15/Config_finale'  # Remplacez cela par votre chemin réel

# Chemin du dossier de destination principal
chemin_dossier_destination = "C:/Users/pc/OneDrive/Documents/projet gns3 fin TD2/projet gns3 fin TD2/project-files/dynamips"

for nom_fic in os.listdir(chemin_dossier_source):
    numero = nom_fic[1:nom_fic.find('_')] 
    dossier_correspondant = nom_fichier[numero]
    chemin_dossier_correspondant = os.path.join(chemin_dossier_destination, dossier_correspondant)
    chemin_configs = os.path.join(chemin_dossier_correspondant, 'configs')
    chemin_destination = os.path.join(chemin_configs, nom_fic)
    shutil.move(os.path.join(chemin_dossier_source, nom_fic), chemin_destination)
