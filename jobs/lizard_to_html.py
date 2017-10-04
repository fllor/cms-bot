#!/usr/bin/env python

import argparse
import re
import os

# constants
html_start = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
'''

html_end = '''
</body>
</html>
'''

link_root = 'www.github.com/test_link'
a_href = '<a href="{url}">{text}</a>'
table = '''<table class="table-bordered">\n\t{0}\n</table>\n'''
table_start = '''<table class="table-bordered">\n'''
table_end = '''</table>\n'''

tr = '<tr>\n{0}\n</tr>\n'  # row
th = '<th>{0}</th>'  # label column
td = '<td>{0}</td>'  # column
h1 = '<h1>t{0}\n</h1>\n'

# regex
regex_dashes = '^(-|=)*$'
regex_td = '^[ ]*[\d *]+.*\..+$'
# regex_th = '^[^\d\W]+$'
regex_th = '.*(NLOC|Total nloc)'
regex_H1_warnings = ' *^!+.*!+ *$'
regex_H1_no_warnings = 'No thresholds exceeded \('
regex_H1_files = '^\d+ file analyzed'
regex_split = "[ ]{2,}|[ ]*$]"
regex_split_td = "[ ]{1,}|[ ]*$]"



def format_tag(tag, value):
    return tag.format(value)


def format_a_ref(url, text):
    return a_href.format(url=url, text=text)


#
#
# def format_html(title, content):
#     return html.format(title=title, content=content)


def get_args():
    '''This function parses and return arguments passed in'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Script converts lizard .txt output to .html')

    # Add arguments
    parser.add_argument(
        '-s', '--source', type=str, help='Source file', required=True)
    parser.add_argument(
        '-d', '--dir', type=str, help='Output directory', required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Assign args to variables
    source = args.source
    output_d = args.dir

    # Return all variable values
    return source, output_d


total_col_nr = 0 # global value


def parse(file, line_previous, line):
    global total_col_nr

    if bool(re.search(regex_dashes, line)):
        return False

    elif bool(re.search(regex_th, line)):
        table_header_values = re.split(regex_split, line.strip())
        header_table = ''
        for th_val in table_header_values:
            header_table += th.format(th_val)
        file.write(
            tr.format(header_table)
        )
        total_col_nr = len(table_header_values) - 1
        return False

    elif bool(re.search(regex_td, line)):
        table_row_values = re.split(regex_split_td, line.strip(), maxsplit=total_col_nr)
        header_table = ''
        for td_val in table_row_values:
            header_table += td.format(td_val)
        file.write(
            tr.format(header_table)
        )
        return False

    elif bool(re.search(regex_H1_files, line)):
        return True

    return False


def main(source_f_path, output_d):
    """Main function"""

    with open(source_f_path, 'r') as source_f:

        do_split = False
        previous_line = None

        html_0 = open(os.path.join(output_d, 'all_functions.html'), 'w')
        html_0.write(html_start.format(title='all_functions'))
        html_0.write(table_start)
        while do_split is False:
            line = source_f.readline()
            do_split = parse(html_0, previous_line, line)
            previous_line = line
            if not line:
                break
        html_0.write(table_end)
        html_0.write(html_end)
        html_0.close()
        # close open

        # open

        # open document to read

        # open document to write

        # open document


if __name__ == '__main__':
    main(get_args())
