import logging
from typing import Any

import openpyxl
from openpyxl.utils import coordinate_to_tuple

logger = logging.getLogger(__name__)


class ExcelUtil:
    """Utility class for handling Excel files."""

    @staticmethod
    def read_elements_from_table(
        excel_path: str,
        sheet_name: str,
        table_name: str,
        range: str = "",
        contains_header: bool = True,
        headers: list[str] = []
    ) -> list[dict[str, Any]]:
        """Reads rows from a table in an Excel file and returns a list of dictionaries."""
        elements: list[dict[str, Any]] = []
        workbook = openpyxl.load_workbook(excel_path)
        sheet = workbook[sheet_name]
        table = sheet.tables[table_name]
        if not range:
            range = table.ref
            
        start_idx = 0
        if contains_header:
            header_row = sheet[range][0]
            headers = [cell.value for cell in header_row]
            start_idx = 1  # Skip the header row
        
        for row in sheet[range][start_idx:-1]:
            row_data = (
                dict(zip(headers, [cell.value for cell in row]))
                if headers
                else {f"Column_{i+1}": cell.value for i, cell in enumerate(row)}
            )
            elements.append(row_data)
        workbook.close()
        return elements
    
    @staticmethod
    def add_row_elements_to_table(
        excel_path: str,
        sheet_name: str,
        table_name: str,
        row_data_list: list[dict[str, Any]],
        range: str = "",
        coordinates: tuple[int, int] | None = None,
        headers: list[str] = [],
        banned_headers: list[str] = []
    ) -> None:
        """Adds a new row to a table in an Excel file."""
        workbook = openpyxl.load_workbook(excel_path)
        sheet = workbook[sheet_name]
        table = sheet.tables[table_name]
        
        if not range:
            range = table.ref
        
        x_cord, y_cord = coordinate_to_tuple(range.split(":")[0])
        
        row = x_cord + coordinates[0] if coordinates else x_cord + 1
        column = y_cord + coordinates[1] if coordinates else y_cord + 1
        
        if not headers:
            headers = [col.name for col in table.tableColumns]

        for row_index, row_data in enumerate(row_data_list, start=row):
            for col_index, header in enumerate(headers, start=column):
                if header in banned_headers:
                    continue
                cell = sheet.cell(row=row_index, column=col_index)
                cell.value = row_data.get(header, "")

        workbook.save(excel_path)
        workbook.close()
