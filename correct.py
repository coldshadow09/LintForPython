import lint
import utils
import string

def correct_single_char(tuple):
    errortype, line_number, column_number, info, line = tuple
    new_line = ''
    index = 0
    for char in line:
        index += 1
        if index != column_number:
            new_line += char
        else:
            new_line += 'var_' + char
    new_tuple = (line_number, new_line)
    return new_tuple

def correct_long_line(tuple):
    errortype, line_number, column_number, info, line = tuple
    line1 = ''
    line2 = ''
    for char in line:
        if len(line1) <= 76:
            line1 += char
        else:
            line2 += char
    new_line = line1 + ' \\' +'\n' + line2
    new_tuple = (line_number, new_line)
    return new_tuple

def correct_trail_whitespace(tuple):
    errortype, line_number, column_number, info, line = tuple
    new_line = ''
    for char in line:
        if len(new_line) != column_number - 1:
            new_line += char
        else:
            break
    new_tuple = (line_number, new_line)
    return new_tuple

def correct_bad_indent(tuple):
    errortype, line_number, column_number, info, line = tuple
    new_line = ''
    indents = line[:column_number]
    new_indent = ''
    for space in indents:
        new_indent += space
    if len(new_indent) % 4 != 0:
        new_indent += ' '
    else:
        new_line += new_indent
        for char in line[column_number:]:
            new_line += char
    new_tuple = (line_number, new_line)
    return new_tuple
    
def correct_all_errors(file_name):
    allerrors = lint.all_errors(file_name)
    result = []
    for tuple in allerrors:
        errortype = tuple[0]
        if errortype == 'SINGLE_CHAR_VAR':
            new_tuple = correct_single_char(tuple)
            result.append(new_tuple)
        if errortype == 'LONG_LINE':
            new_tuple = correct_long_line(tuple)
            result.append(new_tuple)
        if errortype == 'TRAIL_WHITESPACE':
            new_tuple = correct_trail_whitespace(tuple)
            result.append(new_tuple)
        if errortype == 'BAD_INDENT':
            new_tuple = correct_bad_indent(tuple)
            result.append(new_tuple)
    return result

def replace_lines(file_name):
    all_lines = lint.stripped_file(file_name)
    all_errors = correct_all_errors(file_name)
    for line in all_lines:
        for tuple in all_errors:
            line_number, new_line = tuple
            if line == line_number:
                all_lines[line_number] = new_line
    return all_lines

def correct(file_name):
    prefix = file_name[:-3]
    output = prefix + 'correct.py'
    file = open (output, 'w')
    all_lines = replace_lines(file_name)
    for line_number in all_lines:
        line = all_lines[line_number]
        line +='\n'
        file.write(line)
    file.close()
    return None

