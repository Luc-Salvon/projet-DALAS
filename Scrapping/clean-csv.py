import numpy as np
import pandas as pd

df = pd.read_csv("../Donnees/game_data.csv")
df = df.set_index("hltb_id")


# Prix
def traitement_prix(prix):
    prix = str(prix)

    if prix == "nan":
        return

    if prix[0] == '$':
        if len(prix) == 1:
            return
        return float(prix[1:]) * .92

    if prix[-1] == "€":
        return float(prix[:-1].replace(",", ".").replace("-", "0"))

    if prix in {"Gratuit", "Free-to-play", "Free to Play", "Install Now", "Free To Play", "Gratuit !", "Free Mod"}:
        return 0.

    print(f"PRIX NON TRAITE : {prix}")
    return


def traitement(dfcol, f):
    remplacement = np.zeros(len(dfcol))

    for i, el in enumerate(dfcol):
        remplacement[i] = f(el)

    return remplacement


df["price"] = traitement(df["price"], traitement_prix)

df.to_csv("../Donnees/cleaned_data.csv")