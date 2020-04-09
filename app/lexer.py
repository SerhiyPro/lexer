from dataclasses import dataclass, field
from .enums import Lexems


@dataclass
class Lexer:
    """
    Class that performs lexical analysis
    """
    input_lines: dict = field(default_factory=dict)
    current_line_number: int = 0
    head_position: int = 0
    comma_dividers: tuple = ('\n', '\t')
    beginners: tuple = ('', ' ', '\n', '\\', '<')
    input_file_name: str = 'data_files/input.txt'
    output_file_name: str = 'data_files/output.txt'

    def clean_output_file(self):
        with open(self.output_file_name, 'w') as file:
            print('The output file has successfully been cleaned')

    def get_input_data(self):
        with open(self.input_file_name) as file:
            for line_number, line in enumerate(file):
                self.input_lines[line_number] = line

    def write_lexem_to_file(self, lexem_type, lexem, error_type=''):
        display_message = f'<{lexem_type} \'{lexem}\'>\n' if not error_type else \
         f'<error in sentence {self.current_line_number} in position {self.head_position}, {error_type}>\n'
        with open(self.output_file_name, 'a') as file:
            file.write(display_message)
        print(display_message)

    def get_current_symbol(self):
        line = self.input_lines.get(self.current_line_number)

        if self.current_line_number >= len(self.input_lines.keys()):
            return ''
        
        if self.head_position > len(line) - 1:
            self.head_position = 0
            self.current_line_number += 1
            return self.get_current_symbol()
        else:
            current_symbol = line[self.head_position]
            self.head_position += 1
            return current_symbol

    def return_head(self):
        self.head_position -= 1
    
    def get_token(self):
        current_symbol = self.get_current_symbol()

        if current_symbol == '':
            print('We have reached the end of the program!')
            return
        elif current_symbol == '<':
            self.process_tag()
        elif current_symbol == '\\':
            self.process_comma()
        elif current_symbol in Lexems.digit_5.value:
            self.process_digit(current_symbol)
        elif current_symbol == '\n':  # standard end of the line in file
            self.head_position += 1
            self.get_token()
        else:
            self.write_lexem_to_file('', '', f"unknown symbol '{current_symbol}'")

    def process_tag(self):
        tag = f'<{self.get_current_symbol()}'
        next_symbol = self.get_current_symbol()
        while next_symbol not in (*Lexems.digit_5.value, *self.beginners):
            tag = f'{tag}{next_symbol}'
            next_symbol = self.get_current_symbol()
        self.return_head()

        if tag[-1] != '>':
            self.write_lexem_to_file('', '', 'missing closing tag')
            return self.get_token()

        for lexem in Lexems:
            if lexem.value == tag:
                self.write_lexem_to_file(lexem.name, lexem.value)
                return self.get_token()
        
        self.write_lexem_to_file('', '', 'wrong tag')
        return self.get_token()

    def process_comma(self):
        symbol = self.get_current_symbol()
        comma = f'\\{symbol}'

        if comma == '\\n':
            self.write_lexem_to_file('Comma', 'next line')
            return self.get_token()
        elif comma == '\\t':
            self.write_lexem_to_file('Comma', 'tabulation')
            return self.get_token()

        self.write_lexem_to_file('', '', 'wrong divider(coma)')
        return self.get_token()

    def process_digit(self, current_number):
        if current_number == 0:
            self.write_lexem_to_file('5-digit divisible number', 0)
        else:
            symbol = self.get_current_symbol()
            number = current_number
            while symbol in Lexems.digit_5.value:
                number = number + symbol
                symbol = self.get_current_symbol()
            if number[-1] == '0':
                self.write_lexem_to_file("5-digit divisible number", number)
            else:
                self.write_lexem_to_file('', '', 'number is not divisible by 5')
            self.return_head()
        return self.get_token()
