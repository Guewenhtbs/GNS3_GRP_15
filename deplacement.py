import os
import os
import shutil

# Dictionnaire des correspondances entre numéro et UUID
nom_fichier = {
    "2": "fe0ba0e8-6a04-4df7-9313-3e6fae359fa8",
    "5": "e77dcbd6-4836-468f-a13e-a217f926ebe3",
    "7": "e832c8a7-6a47-445e-b387-e5131f76e1a7"
}

# Chemin du dossier contenant les fichiers .txt
chemin_dossier_source = 'C:/Users/pc/OneDrive/Documents/GNS3/GNS3_GRP_15/Config_test'  # Remplacez cela par votre chemin réel

# Chemin du dossier de destination principal
chemin_dossier_destination = 'C:/Users/pc/Downloads/projet gns3 fin TD2/projet gns3 fin TD2/project-files/dynamips/'

# Parcourir tous les fichiers du dossier source
for nom_fic in os.listdir(chemin_dossier_source):
    print(nom_fic)
    # Vérifier si le fichier est un fichier .txt
    if nom_fic.endswith('.txt'):
        # Extraire le numéro du nom de fichier
        numero = os.path.splitext(nom_fic)[0][1:]
        
        # Vérifier si le numéro est une clé du dictionnaire
        if numero in nom_fichier:
            correspondance = nom_fichier[numero]
            
            # Chemin complet du dossier de destination correspondant à la correspondance UUID
            chemin_dossier_correspondant = os.path.join(chemin_dossier_destination, correspondance)
            
            # Créer le dossier s'il n'existe pas déjà
            if not os.path.exists(chemin_dossier_correspondant):
                os.makedirs(chemin_dossier_correspondant)
            
            # Chemin complet du fichier texte source
            chemin_source = os.path.join(chemin_dossier_source, nom_fic)
            
            # Chemin complet du fichier texte de destination
            chemin_destination = os.path.join(chemin_dossier_correspondant, nom_fic)
            
            # Déplacer le fichier texte vers le dossier correspondant
            shutil.move(chemin_source, chemin_destination)
            print(f"Fichier {nom_fic} déplacé vers {chemin_dossier_correspondant}")

# récupérer le numéro du routeur avec le nom final
# remplacer le fichier dans la destination plutôt que juste le copier
# le mettre dans le fichier configs

"""

nom_fichier : {
    #"1" : "39a09daf-6bbb-49d2-bdef-bdece8410620",
    "2" : "fe0ba0e8-6a04-4df7-9313-3e6fae359fa8",
    #"3" : "a1c19efa-228a-48e5-8a1d-823304341d74",
    #"4" : "75775339-44a9-4691-b549-9a79b4a4bfeb",
    "5" : "e77dcbd6-4836-468f-a13e-a217f926ebe3",
    #"6": "08ab2678-0b8c-4c30-8ed6-b98c4fdc7bb4",
    "7": "e832c8a7-6a47-445e-b387-e5131f76e1a7",
    "8" : "e832c8a7-6a47-445e-b387-e5131f76e1a7",
    #"9" : "15c3dfa8-cb83-4f97-b3cc-dc12aefd0783",
    "10" : "852a964a-91e6-4e41-8fb2-4cbb3fc387c8",
    #"11" : "6228e624-4df2-4960-bc5e-18c4b13a3902",
    "12" : "ee6eb131-eaa9-4247-a5c4-5e0522e20f51",
    #13" : "92fd3895-4db0-4412-8d46-d2cc9be695db",
    #14" : "acdcac23-67fc-40b3-9fbe-a495b49e42f5"
}

# Chemin du dossier contenant les fichiers .txt
chemin_dossier = '/Config_test/'  # Remplacez cela par votre chemin réel

# Parcourir tous les fichiers du dossier
for nom_fic in os.listdir(chemin_dossier):
    # Vérifier si le fichier est un fichier .txt
    if nom_fic.endswith('.txt'):
        # Extraire le numéro du nom de fichier
        numero = os.path.splitext(nom_fic)[0][1:]
        
        # Vérifier si le numéro est une clé du dictionnaire
        if numero in nom_fichier:
            correspondance = nom_fichier[numero]
            print(f"Correspondance trouvée pour {nom_fic} : {correspondance}")

"""