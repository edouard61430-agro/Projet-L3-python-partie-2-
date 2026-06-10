import geopandas as gpd
import numpy as np

try:
    land_use = gpd.read_file('CLC_RARA_RGF_SHP/CLC90/CLC90_RARA_RGF.shp')
except FileNotFoundError:
    raise FileNotFoundError("Le fichier n'existe pas au lien donné.")

print("ça marche !")


classes = np.unique(land_use['CODE_90'])
nb_class_dist = len(classes)
print(nb_class_dist)

occurences = np.array([
    (land_use['CODE_90'] == c).sum()
    for c in classes
])
print(occurences)

def get_agg_code(fichier: gpd.GeoDataFrame, colonne: str) -> np.ndarray:
    """
    Agrège les codes d'une colonne en conservant uniquement leur premier chiffre.

    Paramètres :
        fichier : geopandas.GeoDataFrame
        GeoDataFrame contenant les données.
    colonne : str
        Nom de la colonne contenant les codes à agréger.

    Retourne : 
        np.ndarray
        Tableau NumPy contenant les codes agrégés sur un chiffre.
    Lève :
        TypeError
            Si fichier n'est pas un GeoDataFrame.
        KeyError
            Si la colonne n'est pas présente dans le GeoDataFrame.
    """

    if not isinstance(fichier, gpd.GeoDataFrame):
        raise TypeError("Le paramètre 'fichier' doit être un GeoDataFrame.")

    if colonne not in fichier.columns:
        raise KeyError(f"La colonne '{colonne}' est absente.")

    # Convertit la colonne en format str et 
    # agrège alors les chaînes de caractères en conservant uniquement le premier caractère
    fichier[colonne] = fichier[colonne].astype(str).str[0]
    
    #Convertit à nouveau en chiffre afin d'avoir le code en format numérique
    fichier[colonne] = fichier[colonne].astype(int)

    return fichier

land_use = get_agg_code(land_use, 'CODE_90')
print(land_use.head())