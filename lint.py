import utils
import csv

def stripped_file(file_name):
    '''
    +--------+
    | Output |
    +--------+
    A dictionary containing all the lines in the source code with a line
    number starting from line 1.
     { line_number: source line}

    +-----------+
    | Parameter |
    +-----------+
    A string of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Strips the '\n' and '\r' characters of the file as they are not
    included in the consideration of the length of a line.

    '''
    file = open(file_name)
    all_lines = {}
    # Counts the line number from 1
    line_counter = 1
    for line in file:
        stripped_line = line.rstrip('\n\r')
        all_lines[line_counter] = stripped_line
        # As the newline characters and return characters are
        # stripped off the line, the line number is incremented by 1
        line_counter += 1
    file.close()
    return all_lines

def single_char_var(file_name):
    '''
    +--------+
    | Output |
    +--------+
    A list of tuples containing the error type, line number, column number
    of the first and only character of the variable name, variable name,
    and line in the source code

    +-----------+
    | Parameter |
    +-----------+
    A string of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Reports the variable names consisting of a single character.
    All repeated single character variables on the same line are also
    reported.

    '''
    result = []
    # Calls the vars_indents function in the utils module
    # to retrieve the dictionary containing variables
    variables_dict = utils.vars_indents(file_name)[0]
    all_lines = stripped_file(file_name)
    error_type = 'SINGLE_CHAR_VAR'
    for line_number in variables_dict:
        list = variables_dict[line_number]
        line = all_lines[line_number]
        for tuple in list:
            variable, col_number = tuple
            # If the variable is a single character, a tuple is created
            # and appended to a list
            if len(variable) == 1:
                detail = (error_type, line_number, col_number, variable, line)
                result.append(detail)
    return result

def long_line(file_name):
    '''
    +--------+
    | Output |
    +--------+
    A list of tuples containing the error type, line number, None type, length
    of line, and line in the source code
    # Note: None type is used in the column of the <prefix>.lint.csv file as
    there is no column number for a long line.

    +-----------+
    | Parameter |
    +-----------+
    A string of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Reports the lines that contains more than 79 characters.

    '''
    all_lines = stripped_file(file_name)
    result = []
    error_type = 'LONG_LINE'
    for line_number in all_lines:
        line = all_lines[line_number]
        line_length = len(line)
        # If the length of the line exceeds 79 characters, a tuple
        # is created and appended to a list
        if line_length > 79:
            detail = (error_type, line_number, None, line_length, line)
            result.append(detail)
    return result

def get_first_whitespace(line):
    '''
    +--------+
    | Output |
    +--------+
    An integer of the first column number of the trailing whitespace character
    in the corresponding line

    +-----------+
    | Parameter |
    +-----------+
    A string of a line of source code

    +----------+
    | Function |
    +----------+
    Gets the column of the first column number by testing if the character
    is a space (' ') or a tab ('\t') character.

    '''
    number_cols = len(line)
    count = 0
    for char in line[::-1]:
        if char in ' \t':
            count += 1
        else:
            break
    col_number = number_cols - count + 1
    return col_number

def trail_whitespace(file_name):
    '''
    +--------+
    | Output |
    +--------+
    A list of tuples containing the error type, line number, column position
    of first trailing whitespace, None type, and line in the source code
    # Note: None type is used in the INFO column of the <prefix>.lint.csv
    file as it is an empty field

    +-----------+
    | Parameter |
    +-----------+
    A string of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Reports the lines that contains space or tab characters immediately before
    the end of a line
    
    '''
    all_lines = stripped_file(file_name)
    result = []
    error_type = 'TRAIL_WHITESPACE'
    for line_number in all_lines:
        line = all_lines[line_number]
        # If the end of the line contains spaces or tab characters,
        # a tuple is created and appended to a list
        if line.endswith(' ') or line.endswith('\t'):
            col_number = get_first_whitespace(line)
            detail = (error_type, line_number, col_number, None, line)
            result.append(detail)
    return result

def bad_indent(file_name):
    '''
    +--------+
    | Output |
    +--------+
    A list of tuples containing the error type, line number, column position
    of first character immediately after indentation, None type, and line in
    the source code
    # Note: None type is used in the INFO column of the <prefix>.lint.csv
    file as it is an empty field
    
    +-----------+
    | Parameter |
    +-----------+
    A string of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Reports the lines that has an indentation that is not a multiple of 4
    single spaces, inclusive of tab characters

    '''
    # Calls the vars_indents function in the utils module
    # to retrieve the dictionary containing indentations
    indents_dic = utils.vars_indents(file_name)[1]
    all_lines = stripped_file(file_name)
    result = []
    error_type = 'BAD_INDENT'
    for line_number in indents_dic:
        indents, end_col = indents_dic[line_number]
        line = all_lines[line_number]
        # Number of single spaces is before the column position
        col_indents = end_col - 1
        # If the number of spaces is not a multiple of 4,
        # a tuple is created and appended to a list
        if col_indents % 4 != 0:
            detail = (error_type, line_number, end_col, None, line)
            result.append(detail)
    return result

def all_errors(file_name):
    '''
    +--------+
    | Output |
    +--------+
    A list of tuples containing the error type, line number, column number,
    info, and line in the source code

    +-----------+
    | Parameter |
    +-----------+
    A string of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Gets all the errors in the file and arrange them in ascending line number

    '''
    single_char_errors = single_char_var(file_name)
    long_line_errors = long_line(file_name)
    trail_whitespace_errors = trail_whitespace(file_name)
    bad_indent_errors = bad_indent(file_name)
    result = []
    for tuple in single_char_errors:
        result.append(tuple)
    for tuple in long_line_errors:
        result.append(tuple)
    for tuple in trail_whitespace_errors:
        result.append(tuple)
    for tuple in bad_indent_errors:
        result.append(tuple)
    # All the errors are sorted by the line number
    result.sort(key = lambda detail: detail[1])
    return result

def error_file(file_name):
    '''
    +--------+
    | Output |
    +--------+
    None

    +-----------+
    | Parameter |
    +-----------+
    A string of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Creates a CSV file containing the summary of all the style errors made in
    the input file

    '''
    prefix = file_name[:-3]
    out_name = prefix + '.lint.csv'
    csv_file = open (out_name, "w")
    allerrors = all_errors(file_name)
    header = [('ERROR_TYPE', 'LINE_NUMBER', 'COLUMN', 'INFO', 'SOURCE_LINE')]
    writer = csv.writer(csv_file)
    writer.writerows(header)
    # A container is used to make a sequence for writing a row in the CSV file
    for tuple in allerrors:
        container = []
        container.append(tuple)
        writer.writerows(container)
    csv_file.close()

def count_score(file_name):
    '''
    +--------+
    | Output |
    +--------+
    A floating point rounded to 2 decimal places

    +-----------+
    | Parameter |
    +-----------+
    A string of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Calculates the quality score of the style errors made in the input style
    over a score of 10
    '''
    # Gets all the errors made from all_errors function
    allerrors = all_errors(file_name)
    totalpenalty = 0.0
    for tuple in allerrors:
        error_type = tuple[0]
        if error_type == 'TRAIL_WHITESPACE':
            totalpenalty += 1.0
        elif error_type == 'SINGLE_CHAR_VAR':
            totalpenalty += 2.0
        elif error_type == 'BAD_INDENT':
            totalpenalty += 4.0
        elif error_type == 'LONG_LINE':
            totalpenalty += 5.0
    # Number of lines is the number of keys in stripped_file function
    numlines = len(stripped_file(file_name))
    # If the file is empty, a penalty score of 10 is given
    if numlines == 0:
        penalty = 10.0
    else:
        penalty = ((totalpenalty / numlines) * 10)
    qualityscore = max(0, 10 - penalty)
    return round(qualityscore, 2)

def score_file(file_name):
    '''
    +--------+
    | Output |
    +--------+
    A CSV file containing the timestamp of when the lint file is run,
    and the quality score of the input file

    +-----------+
    | Parameter |
    +-----------+
    A string of the prefix of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Creates a CSV file that contains the history of the quality score
    of the input Python file

    '''
    prefix = file_name[:-3]
    score_file = open(prefix + '.score.csv', 'a')
    writer = csv.writer(score_file)
    row = []
    container = []
    timestamp = utils.get_current_date_time()
    qualityscore = count_score(file_name)
    row.append(timestamp)
    row.append(qualityscore)
    container.append(row)
    writer.writerows(container)
    score_file.close()

def lint(file_name):
    '''
    +--------+
    | Output |
    +--------+
    None

    +-----------+
    | Parameter |
    +-----------+
    A string of the prefix of the input Python source code file name

    +----------+
    | Function |
    +----------+
    Checks the styling errors in the input file and creates an error file
    and modifies a quality score log file

    '''
    error = error_file(file_name)
    score = score_file(file_name)
    return None
