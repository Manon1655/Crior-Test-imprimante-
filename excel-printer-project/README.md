# Excel Printer Project

## Overview
The Excel Printer Project is designed to automate the generation of Excel files containing production data and send them to a printer using ESC/P commands. The project integrates with the Odoo environment to retrieve order and line data, format it into an Excel workbook, and manage printing tasks efficiently.

## Project Structure
```
excel-printer-project
├── src
│   ├── main.py               # Entry point for the application
│   ├── config.py             # Configuration settings for the project
│   ├── model
│   │   └── excel.py          # Code for generating the Excel file
│   ├── printer
│   │   ├── __init__.py       # Initializes the printer module
│   │   └── escp.py           # Functions for ESC/P printing
│   └── utils
│       └── odoo_env.py       # Utility functions for Odoo interactions
├── tests
│   └── test_printer.py       # Unit tests for printer functionality
├── requirements.txt           # Project dependencies
├── pyproject.toml            # Project configuration
└── README.md                 # Project documentation
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd excel-printer-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application and generate the Excel file, execute the following command:
```
python src/main.py
```

This will create an Excel file based on the current order data and send the relevant sections to the printer.

## Configuration
Adjust the printer settings and paths in `src/config.py` as needed to match your environment.

## Testing
To run the unit tests for the printer functionality, use:
```
pytest tests/test_printer.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.