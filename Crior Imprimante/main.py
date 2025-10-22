from collections import defaultdict
import pandas as pd
from model.impression_brother_cmd import print_postes_with_cut
import os
import re

def extraire_numero_devis(fichier_excel: str) -> str:
    df_raw = pd.read_excel(fichier_excel, header=None, nrows=10)
    for row in df_raw.itertuples(index=False):
        for cell in row:
            if isinstance(cell, str) and re.match(r"S\d+", cell.strip()):
                return cell.strip().upper()
    return "DEVIS_SANS_NUMERO"

def extraire_articles_par_poste(fichier_excel: str) -> list[tuple[str, str]]:
    df_raw = pd.read_excel(fichier_excel, header=None)
    df_data = df_raw.iloc[9:].reset_index(drop=True)

    articles_by_poste = defaultdict(list)
    poste_courant = None

    for _, row in df_data.iterrows():
        description = str(row[0]).strip() if pd.notna(row[0]) else ""

        is_poste = (
            description != ""
            and not description.startswith("-")
            and not any(char.isdigit() for char in description)
            and description == description.title()
        )

        if is_poste:
            poste_courant = description

        if poste_courant and description.startswith("-"):
            articles_by_poste[poste_courant].append(description)

    return [(poste, "\n".join(lignes)) for poste, lignes in articles_by_poste.items()]


def main():
    dossier = "."  # Dossier contenant les fichiers Excel
    fichiers_xlsx = [f for f in os.listdir(dossier) if f.endswith(".xlsx")]

    if not fichiers_xlsx:
        print("Aucun fichier Excel trouvé.")
        return

    for fichier in fichiers_xlsx:
        chemin = os.path.join(dossier, fichier)
        numero_devis = extraire_numero_devis(chemin)
        print(f"\nTraitement du fichier : {fichier} (Devis: {numero_devis})")

        articles = extraire_articles_par_poste(chemin)

        if not articles:
            print("Aucun article trouvé.")
            continue

        print("Impression en cours...")
        print_postes_with_cut(articles)
        print("Impression terminée.")


if __name__ == "__main__":
    main()
