def send_to_printer(data, printer_path="/dev/usb/lp0"):
    esc = b'\x1B'  # ESC command
    cut_command = b'\x1D\x56\x41\x00'  # ESC/P command for cutting

    with open(printer_path, 'wb') as printer:
        for section in data:
            printer.write(data[section].encode('utf-8'))
            printer.write(esc + b'@')  # Initialize printer
            printer.write(cut_command)  # Send cut command

def print_sections(sections):
    for post_name, content in sections:
        send_to_printer({post_name: content})