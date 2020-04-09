from enum import Enum


class Lexems(Enum):
    """
    Enum that contains basic lexems
    """
    table_open_tag = '<table>'
    table_close_tag = '</table>'
    row_open_tag = '<tr>'
    row_close_tag = '</tr>'
    cell_open_tag = '<td>'
    cell_close_tag = '</td>'
    digit_5 = {'0', '1', '2', '3', '4'}
