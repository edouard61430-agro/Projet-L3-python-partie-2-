import geopandas as gpd


try:
    land_use = gpd.read_file('CLC_RARA_RGF_SHP/CLC90/CLC90_RARA_RGF.shp')
except FileNotFoundError:
    raise FileNotFoundError("Le fichier n'existe pas au lien donné.")

print("ça marche !")