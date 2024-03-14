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



def traitement_description(desc):
    try:
        if desc.strip().split()[0] in {"jeu", "contenu", "logiciel", "te", "équipement"}:
            if desc.startswith("te"):
                space = desc[4:].index(" ")
            else:
                space = desc.index(" ")
            return desc[space + 1:].strip()
        else:
            print(desc[:10])
            return desc.strip()
    except (IndexError, TypeError, AttributeError):
        return ""


def traitement_int(el):
    try:
        return int(el)
    except ValueError:
        return pd.NA


def pourcentage_pos(pour):
    try:
        return int(pour)
    except ValueError:
        return


def traitement(dfcol, f):
    remplacement = [0] * len(dfcol)

    for i, el in enumerate(dfcol):
        remplacement[i] = f(el)

    return remplacement


df["rating"] = traitement(df["rating"], traitement_int)

df["date"] = traitement(df["date"], traitement_int)

df["price"] = traitement(df["price"], traitement_prix)

df["review_count"] = traitement(df["review_count"], traitement_int)

df["description"] = traitement(df["description"], traitement_description)

df["twenty_four_hours"] = traitement(df["twenty_four_hours"], traitement_int)

df["all_time"] = traitement(df["all_time"], traitement_int)

df["pourcentage_pos"] = traitement(df["pourcentage_pos"], traitement_int)

del df["espace_disque"]
del df["memoire_vive"]

df = df.dropna(axis="rows")

df.to_csv("../Donnees/cleaned_data.csv")
