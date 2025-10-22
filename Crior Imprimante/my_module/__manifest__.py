{
    "name": "Crior Imprimante",
    "version": "1.0",
    "category": "Tools",
    "summary": "Module for managing printing tasks with Brother printers.",
    "description": """
        This module provides functionalities for printing tasks,
        including formatting and sending print jobs to Brother printers
        using ESC/P commands.
    """,
    "author": "Crior",
    "website": "https://crior.example.com",
    "license": "LGPL-3",
    "depends": [
        "base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/custom_sale.xml",
        "views/hide_price_zero_line.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False
}
