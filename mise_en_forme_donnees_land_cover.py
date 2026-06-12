import geopandas as gpd
import numpy as np
import pytest
import matplotlib.pyplot as plt
import pandas as pd


def import_land_use(region: str, annee_agg: str):
    '''
    Retourne le fichier importé de la région pour une année donnée

    Paramètres : region: str
                    region souhaité au format str
                    avec son acronyme ('BRE' par exemple)
                annee_agg : str
                    année souhaité au format str
                    aggrégé aux deux derniers chiffre
                    ('90' par exemple)

    Retourne : fichier geopandas du fichier .shp importé

    Lève une erreur si le fichier n'existe pas
    '''
    try:
        land_use = gpd.read_file(
            f"CLC_R{region}_RGF_SHP/CLC{annee_agg}/"
            f"CLC{annee_agg}_R{region}_RGF.shp"
            )
    except FileNotFoundError:
        raise FileNotFoundError("Le fichier n'existe pas au lien donné.")

    return land_use


def get_agg_code(fichier: gpd.GeoDataFrame, colonne: str) -> np.ndarray:
    """
    Agrège les codes d'une colonne en conservant uniquement
    leur premier chiffre.

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
    # agrège alors les chaînes de caractères en conservant
    # uniquement le premier caractère
    fichier[colonne] = fichier[colonne].astype(str).str[0]

    # Convertit à nouveau en chiffre afin d'avoir le code en format numérique
    fichier[colonne] = fichier[colonne].astype(int)

    # Transcrit les codes en libelle
    fichier[colonne] = fichier[colonne].apply(correspondance_code_libelle)

    return fichier


def correspondance_code_libelle(code):
    '''
    Transcrit les codes de la colonne code en noms de catégories définies

    Paramètre : code : int
                        le code est un chiffre entre 1 et 5 inclus.

    Lève une erreur si le code n'appartient pas
    à l'intervalle des entiers de 1 à 5

    Retourne une chaîne caractère str correspondant au code donné
    '''
    dico = {
        1: "Territoires artificialisés",
        2: "Territoires agricoles",
        3: "Forêts et milieux semi-naturels",
        4: "Zones humides",
        5: "Surfaces en eau"
        }

    if code not in dico:
        raise ValueError(f"Le code {code} est inconnu")

    return dico[code]


def test_code():
    '''
    Effectue un test unitaire afin de vérifier que la transcription du code 1
    avec correpondance_code_libelle est bien faite
    Paramètre : Aucun
    Lève une erreur si le test n'est pas réussi
    Retourne : rien
    '''
    assert correspondance_code_libelle(1) == "Territoires artificialisés"


def test_code_invalide():
    '''
    Effectue un test unitaire afin de vérifier que
    la transcription d'un code inconnu avec
    correpondance_code_libelle() renvoie bien une ValueError

    Paramètre : Aucun

    Lève une erreur si le test n'est pas réussi

    Retourne : rien
    '''
    with pytest.raises(ValueError):
        correspondance_code_libelle(6)


def plot_land_cover(region: str = 'all', annee: int = 0):
    '''
    Affiche un diagramme en barre et un diagramme circulaire des
    milieux en ARA en fonction des années

    Paramètres :
    annee au format "float" dans la liste:
    [1990, 2000, 2006, 2012, all] pour les années souhaitées

    Retourne : Rien mais affiche les deux diagrammes
    '''

    # Lève une erreur si l'année n'est pas disponible
    if annee not in [1990, 2000, 2006, 2012, 0]:
        raise ValueError(f"L'année {annee} n'est pas disponible")

    if region not in ['ARA', 'BRE', 'all']:
        raise ValueError(f"La région {region} n'est pas disponible")

    # Crée deux listes contenant les régions et années à étudier
    regions = ['ARA', 'BRE'] if region == 'all' else [region]
    annees = [1990, 2000, 2006, 2012] if annee == 0 else [annee]

    liste_surfaces = []
    # Pour toutes les régions et années sélectionnées,
    for reg in regions:
        for an in annees:
            # on importe le dataframe avec la fonction import_land_use()
            code_annee = str(an)[-2:]
            land_use = import_land_use(reg, code_annee)
            colonne = f"CODE_{code_annee}"

            # !!!Décommenter si on souhaite afficher
            # les données suivant le nom des types de sols
            # land_use = get_agg_code(land_use, colonne)

            # On regroupe par type de sol et somme les surfaces
            surfaces = land_use.groupby(colonne)["AREA_HA"].sum().reset_index()

            # on renome la colonne 'colonne' en "CODE"
            surfaces = surfaces.rename(
                columns={
                    colonne: "CODE"
                }
            )

            # On ajoute le nouveau dataframe à une liste
            liste_surfaces.append(surfaces)

    # on concatène en un dataframe tous les dataframes de la liste
    land_use_total = pd.concat(liste_surfaces, ignore_index=True)

    # on regroupe par type de sol et on calcule
    # la surface moyenne du type de sol
    surfaces_moyennes = (
        land_use_total.groupby("CODE")["AREA_HA"]
        .mean().
        reset_index()
    )

    # On affiche le diagramme en barre des surfaces
    # en fonction des types de sol
    plt.bar(surfaces_moyennes["CODE"], surfaces_moyennes["AREA_HA"])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Occupation du sol en ARA en fonction des années: {annees}")
    plt.tight_layout()
    plt.show()

    # On affiche ensuite le diagramme circulaire des surfaces moyennes
    # en fonction des types de sol
    plt.figure()
    plt.pie(
        surfaces_moyennes["AREA_HA"],
        labels=surfaces_moyennes["CODE"],
        autopct="%1.1f%%"
        )
    plt.title(
        f"Répartition de l'occupation du sol en ARA en fonction des"
        f" années: {annees}"
        )
    plt.show()


# Importation du fichier ARA de 1990
land_use_ara = import_land_use('ARA', '90')

# Création d'un array contenant les types de CODE_90 distincts du dataframe
classes = np.unique(land_use_ara['CODE_90'])

# Création d'une variable comptant le nombre de classes
# distinctes de land_use_ara['CODE_90']
nb_class_dist = len(classes)
print(nb_class_dist)

# On compte le nombre d'occurences de chaque classe
# dans la colonne CODE_90 de land_use_ara
occurences = np.array([
    (land_use_ara['CODE_90'] == c).sum()
    for c in classes
])
print(occurences)

# On effectue les 2 tests unitaires
test_code()
test_code_invalide()

# On affiche les 2 diagrammes pour l'année 2006 en ARA
plot_land_cover('ARA', 2006)
