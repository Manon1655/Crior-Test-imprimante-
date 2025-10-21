from openpyxl import Workbook, load_workbook
from model.impression_brother_cmd import print_postes_with_cut

def read_excel(file_path):
    """
    Lit un fichier Excel et retourne les données sous forme de liste de dictionnaires.
    Chaque dictionnaire représente une ligne du fichier, avec les en-têtes comme clés.
    """
    workbook = load_workbook(file_path)
    sheet = workbook.active
    data = []
    headers = [cell.value for cell in sheet[1]]  # Supposons que la première ligne contient les en-têtes

    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = {headers[i]: row[i] for i in range(len(headers))}
        data.append(row_data)

    return data

def write_excel(file_path, data):
    """
    Écrit des données dans un fichier Excel.
    Les données doivent être une liste de dictionnaires.
    """
    workbook = Workbook()
    sheet = workbook.active

    # Écrire les en-têtes
    headers = data[0].keys()
    sheet.append(headers)

    # Écrire les données
    for item in data:
        sheet.append(item.values())

    workbook.save(file_path)

# Exemple : choisir le chemin d'impression
# Sous Windows : laisser printer_path = None pour utiliser l'imprimante par défaut,
# ou mettre le nom exact de l'imprimante (ex: r"Brother QL-xxxx").
# Sous Linux : ex: printer_path = "/dev/usb/lp0"
printer_path = None  # ou "/dev/usb/lp0" sur Linux

try:
    # self.sections doit être la liste (poste_name, texte)
    if getattr(self, "sections", None):
        print_postes_with_cut(self.sections, printer_path=printer_path)
except Exception as e:
    # Ne fais pas planter le process si l'impression échoue ; logge l'erreur
    import logging
    _logger = logging.getLogger(__name__)
    _logger.exception("Erreur lors de l'impression des postes : %s", e)