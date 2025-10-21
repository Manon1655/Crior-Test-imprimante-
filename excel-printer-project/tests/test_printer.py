import unittest
from unittest.mock import patch, MagicMock
from src.printer.escp import send_to_printer
from src.model.excel import Writer

class TestPrinter(unittest.TestCase):

    @patch('src.model.excel.print_postes_with_cut')
    def test_print_sections(self, mock_print):
        # Mocking the order, config, env, and lines
        mock_order = MagicMock()
        mock_config = MagicMock()
        mock_env = MagicMock()
        mock_lines = MagicMock()

        # Create a Writer instance
        writer = Writer(mock_order, mock_config, mock_env, mock_lines)

        # Simulate sections
        writer.sections = [
            ('Cuisine', 'Content for Cuisine'),
            ('Envoi', 'Content for Envoi')
        ]

        # Call the print function
        writer._print_sections()

        # Check if print_postes_with_cut was called with the correct parameters
        mock_print.assert_called_with(writer.sections, printer_path="/dev/usb/lp0")

    @patch('src.printer.escp.send_to_printer')
    def test_send_to_printer(self, mock_send):
        # Test sending a section to the printer
        section_content = 'Test content for printing'
        send_to_printer(section_content)

        # Assert that the send_to_printer function was called with the correct content
        mock_send.assert_called_with(section_content)

if __name__ == '__main__':
    unittest.main()