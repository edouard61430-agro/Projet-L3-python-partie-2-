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