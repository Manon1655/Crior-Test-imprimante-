{
    "name": "Crior Imprimante",
    "version": "1.0",
    "category": "Tools",
    "summary": "Module for managing printing tasks with Brother printers.",
    "description": "This module provides functionalities for printing tasks, including the ability to format and send print jobs to Brother printers using ESC/P commands.",
    "author": "Your Name",
    "website": "http://yourwebsite.com",
    "depends": [
        "base",
        "reporting"  # Add any other dependencies your module might need
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/custom_sale.xml",
        "views/hide_price_zero_line.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False
}