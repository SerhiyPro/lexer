from app import Lexer

if __name__ == '__main__':

    lexer = Lexer()
    lexer.clean_output_file()
    lexer.get_input_data()

    print('The file consists of:')
    for line in lexer.input_lines.values():
        print(line)

    print('-' * 50)

    lexer.get_token()
