# Crior Imprimante

## Project Overview
Crior Imprimante is a Python project designed to facilitate printing tasks using Brother printers. It integrates various functionalities, including the ability to construct print pages with ESC/P commands and manage sales data through a custom module.

## Directory Structure
The project is organized as follows:

- **my_module/**: Contains the core functionality of the module, including models, views, and security access rules.
  - **models/**: Defines the data models and includes functionality for handling Excel files.
  - **security/**: Contains access control definitions for the models.
  - **views/**: Holds XML files for custom views related to sales.

- **model/**: Contains the printing logic and commands for interacting with Brother printers.
  - **impression_brother_cmd.py**: Implements functions for building and sending ESC/P commands to the printer.

- **requirements.txt**: Lists the required Python packages for the project.

- **README.md**: Provides documentation for the project.

- **.gitignore**: Specifies files and directories to be ignored by version control.

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```

## Usage
To use the printing functionality, ensure that your Brother printer is connected and accessible via the specified device path. You can then call the functions defined in `impression_brother_cmd.py` to send print commands.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.