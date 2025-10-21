ESC = "\x1B"  # Caractère ESC (ASCII 27)

import os
import sys

def esc_seq(cmd: str) -> bytes:
    return (ESC + cmd).encode("latin-1")

def build_escp_page(poste_name: str, content: str) -> bytes:
    """
    Construit une page ESC/P avec le nom du poste et le contenu, suivi d'une coupe automatique.
    """
    cmds = bytearray()
    cmds += esc_seq("@")                        # Réinitialise l'imprimante
    cmds += esc_seq("i" + "a" + chr(0))         # Mode ESC/P
    cmds += esc_seq("!" + chr(0))               # Style police standard

    # Titre du poste
    cmds += (poste_name.upper() + "\n\n").encode("latin-1", "replace")

    # Contenu du poste (produits + quantités)
    for line in content.strip().split("\n"):
        cmds += (line.strip() + "\n").encode("latin-1", "replace")

    cmds += b"\n\n"
    cmds += esc_seq("i" + "C" + chr(1))  # Découpe automatique

    return bytes(cmds)

def _send_windows_printer(data: bytes, printer_name: str | None = None) -> None:
    """
    Envoie RAW au pilote Windows (utilise pywin32). Si pywin32 absent, écrit dans un fichier temporaire.
    """
    try:
        import win32print
    except Exception:
        # pywin32 non disponible -> fallback vers fichier temporaire
        tmp = os.path.join(os.path.expanduser("~"), "printer_raw_output.bin")
        with open(tmp, "wb") as f:
            f.write(data)
        raise RuntimeError(f"pywin32 non installé. Données écrites dans {tmp}")

    printer_name = printer_name or win32print.GetDefaultPrinter()
    hprinter = None
    try:
        hprinter = win32print.OpenPrinter(printer_name)
        # doc info: (name, output_file, datatype)
        doc = ("Odoo ESC/P Print", None, "RAW")
        win32print.StartDocPrinter(hprinter, 1, doc)
        win32print.StartPagePrinter(hprinter)
        win32print.WritePrinter(hprinter, data)
        win32print.EndPagePrinter(hprinter)
        win32print.EndDocPrinter(hprinter)
    finally:
        if hprinter:
            win32print.ClosePrinter(hprinter)

def send_to_printer_raw(device_path: str | None, data: bytes):
    """
    Envoie les données ESC/P à l’imprimante.
    - Sous Windows, device_path peut être None (utilise imprimante par défaut) ou le nom de l'imprimante.
    - Sous Linux, device_path est typiquement "/dev/usb/lp0".
    """
    if os.name == "nt":
        # Windows
        try:
            _send_windows_printer(data, device_path)
            print(f"✅ Impression envoyée à l'imprimante Windows '{device_path or 'DEFAULT'}'")
        except Exception as e:
            print(f"❌ Erreur d'envoi vers imprimante Windows : {e}")
            raise
    else:
        # Unix-like: écriture directe sur le device_file
        if not device_path:
            raise ValueError("device_path requis sur les systèmes non-Windows (ex: /dev/usb/lp0)")
        try:
            with open(device_path, "wb") as printer:
                printer.write(data)
            print(f"✅ Impression envoyée à {device_path}")
        except Exception as e:
            print(f"❌ Erreur d'impression : {e}")
            raise

def print_postes_with_cut(postes: list, printer_path=None, delay: float = 1.0):
    """
    Imprime chaque poste avec découpe automatique.
    - postes: liste de tuples (poste_name, texte)
    - printer_path:
        * Sous Windows: None -> imprimante par défaut, ou nom de l'imprimante.
        * Sous Linux: chemin device, ex: '/dev/usb/lp0'
    """
    import time
    for poste_name, content in postes:
        page = build_escp_page(poste_name, content)
        send_to_printer_raw(printer_path, page)
        time.sleep(delay)  # Pause entre chaque découpe

# API exportée
__all__ = ["build_escp_page", "send_to_printer_raw", "print_postes_with_cut"]