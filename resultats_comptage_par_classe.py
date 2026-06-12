from mise_en_forme_donnees_land_cover import import_land_use, get_agg_code
import pandas as pd
import numpy as np

def calcul_surface(region: str, annee:int):
    '''
    Calcule la surface et de chaque classe pour la région et l'année données
    et renvoie le résultat sous forme d'une ligne au format dictionnaire

    Paramètres : region : str
                            Acronyme de la région voulue (ex : 'BRE')
                annee : int
                            Année voulue au format int parmi (1990, 2000, 2006, 2012)
    
    Retourne : dictionnaire contenant les clés suivantes : 
        année, région et les classes des sols avec les surfaces en tant que valeurs
    
    Lève des erreurs selon les fonctions import_land_use() et get_agg_code()
    '''
    # Aggrège l'année sous forme de son code pour accéder aux données
    code_annee = str(annee)[-2:]
    # Création de la variable contenant le nom de la colonne
    colonne = f"CODE_{code_annee}"

    # Importation du fichier de la région et de l'année donnée
    land_use = import_land_use(region, code_annee)
    # Transcription des classes de sols dans leurs noms correspondants
    land_use = get_agg_code(land_use, colonne)

    # On somme les surfaces par classe de sols, .reset_index() permet de retrouver le format pd.Dataframe
    area = land_use.groupby(colonne)["AREA_HA"].sum().reset_index()

    # Création du dictionnaire de la ligne initialisé avec la région et l'année
    ligne = {"annee": annee, "région": region}

    # Pour chaque ligne ou classe du dataframe area on ajoute au dictionnaire avec
    # pour clé le nom de la classe et la surface pour valeur.
    for index, row in area.iterrows():
        ligne[row[colonne]] = row["AREA_HA"]
    
    return ligne

calcul_surface("BRE", 2006)





resultats = []

# On récupère les données pour les régions et années suivantes
regions = ["ARA", "BRE"]
annees = [1990, 2000, 2006, 2012]

# On ajoute à la liste resultats chaque ligne contenant les surfaces pour chaque année et région
for reg in regions:
    for an in annees:
        resultats.append(calcul_surface(reg, an))

# On met la liste au format dataframe
df_resultats = pd.DataFrame(resultats)
df_resultats

np.save("areas.npy", df_resultats.to_numpy())