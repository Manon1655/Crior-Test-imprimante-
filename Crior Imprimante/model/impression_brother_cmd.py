import os
import logging
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)

ESC = "\x1B"  # Caractère ESC (ASCII 27)

# Constantes ESC/P
RESET = "@"
ESC_P_MODE = "ia" + chr(0)
STANDARD_STYLE = "!" + chr(0)
CUT_PAPER = "iC" + chr(1)


def esc_seq(cmd: str) -> bytes:
    """Construit une séquence ESC/P en bytes."""
    return (ESC + cmd).encode("latin-1")


def build_escp_page(poste_name: str, content: str) -> bytes:
    """
    Construit une page ESC/P avec le nom du poste et le contenu, suivie d'une coupe automatique.
    """
    cmds = bytearray()
    cmds += esc_seq(RESET)                     # Réinitialise l'imprimante
    cmds += esc_seq(ESC_P_MODE)                # Mode ESC/P (si supporté)
    cmds += esc_seq(STANDARD_STYLE)            # Style police standard

    cmds += (poste_name.upper() + "\n\n").encode("latin-1", "replace")

    for line in content.strip().splitlines():
        cmds += (line.strip() + "\n").encode("latin-1", "replace")

    cmds += b"\n\n"
    cmds += esc_seq(CUT_PAPER)                 # Commande de coupe

    return bytes(cmds)


def _send_windows_printer(data: bytes, printer_name: Optional[str] = None) -> None:
    """
    Envoie les données RAW à une imprimante Windows via pywin32.
    En cas d'absence de pywin32, écrit les données dans un fichier temporaire.
    """
    try:
        import win32print
    except ImportError:
        tmp = os.path.join(os.path.expanduser("~"), "printer_raw_output.bin")
        try:
            with open(tmp, "wb") as f:
                f.write(data)
            logger.warning("pywin32 non installé. Données écrites dans %s", tmp)
        except Exception as io_exc:
            logger.exception("Erreur d'écriture dans le fichier temporaire : %s", io_exc)
            raise
        return

    printer_name = printer_name or win32print.GetDefaultPrinter()
    try:
        hprinter = win32print.OpenPrinter(printer_name)
        try:
            win32print.StartDocPrinter(hprinter, 1, ("Odoo ESC/P Print", None, "RAW"))
            win32print.StartPagePrinter(hprinter)
            win32print.WritePrinter(hprinter, data)
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
            logger.info("Impression envoyée à l'imprimante Windows '%s'", printer_name)
        finally:
            win32print.ClosePrinter(hprinter)
    except Exception:
        logger.exception("Erreur lors de l'envoi à l'imprimante Windows '%s'", printer_name)
        raise


def send_to_printer_raw(device_path: Optional[str], data: bytes) -> None:
    """
    Envoie les données ESC/P à l’imprimante.
    - Windows : device_path peut être None (imprimante par défaut) ou le nom de l'imprimante.
    - Unix : device_path requis (ex: /dev/usb/lp0).
    """
    if os.name == "nt":
        _send_windows_printer(data, device_path)
    else:
        if not device_path:
            raise ValueError("device_path requis sous Linux/Unix (ex: /dev/usb/lp0)")
        try:
            with open(device_path, "wb") as printer:
                printer.write(data)
            logger.info("Impression envoyée à %s", device_path)
        except Exception:
            logger.exception("Erreur d'impression vers %s", device_path)
            raise


def print_postes_with_cut(
    postes: List[Tuple[str, str]],
    printer_path: Optional[str] = None,
    delay: float = 1.0
) -> None:
    """
    Imprime chaque poste avec découpe automatique.
    - postes: liste de tuples (poste_name, texte)
    - printer_path: nom de l'imprimante Windows ou chemin du device Unix
    """
    import time

    if not postes:
        logger.debug("Aucune section à imprimer.")
        return

    for poste_name, content in postes:
        try:
            page = build_escp_page(poste_name, content)
            send_to_printer_raw(printer_path, page)
            time.sleep(delay)
        except Exception:
            logger.exception("Erreur d'impression pour le poste '%s'", poste_name)
            # Continue sur les suivants


__all__ = ["build_escp_page", "send_to_printer_raw", "print_postes_with_cut"]
