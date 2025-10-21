import io
from model.excel import Writer
from printer.escp import send_to_printer
from utils.odoo_env import get_order_and_lines
from config import PRINTER_PATH

def main():
    # Retrieve order and lines from the Odoo environment
    order, lines = get_order_and_lines()

    # Create an instance of the Writer class to generate the Excel file
    writer = Writer(order, config=None, env=None, lines=lines)

    # Retrieve sections by post
    sections = writer.sections

    # Send each section to the printer with automatic cutting
    for post_name, content in sections:
        send_to_printer(content, post_name, PRINTER_PATH)

if __name__ == "__main__":
    main()