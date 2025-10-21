ESC = "\x1B"  # Caractère ESC (ASCII 27)

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
    cmds += (poste_name.upper() + "\n\n").encode("latin-1")

    # Contenu du poste (produits + quantités)
    for line in content.strip().split("\n"):
        cmds += (line.strip() + "\n").encode("latin-1")

    cmds += b"\n\n"
    cmds += esc_seq("i" + "C" + chr(1))  # Découpe automatique

    return cmds

def send_to_printer_raw(device_path: str, data: bytes):
    """
    Envoie les données ESC/P directement à l’imprimante Brother via le port (ex: /dev/usb/lp0)
    """
    try:
        with open(device_path, "wb") as printer:
            printer.write(data)
        print(f"✅ Impression envoyée à {device_path}")
    except Exception as e:
        print(f"❌ Erreur d'impression : {e}")

def print_postes_with_cut(postes: list, printer_path="/dev/usb/lp0"):
    """
    Imprime chaque poste avec découpe automatique.
    - postes: liste de tuples (poste_name, texte)
    - printer_path: port RAW de l’imprimante Brother
    """
    import time
    for poste_name, content in postes:
        page = build_escp_page(poste_name, content)
        send_to_printer_raw(printer_path, page)
        time.sleep(1)  # Pause entre chaque découpe
