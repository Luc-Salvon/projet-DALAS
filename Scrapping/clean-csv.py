import pandas as pd

df = pd.read_csv("../Donnees/game_data.csv")
df = df.set_index("hltb_id")



df.to_csv("../Donnees/cleaned_data.csv")
