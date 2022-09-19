import cryptocode
import os

from pathlib import Path

keyword = 'bananna'

def list_files():
    """List all files inside a folder.

    Args:
        file_path: the folder path as string
    Returns:
        A list.
    """
    return sorted(next(os.walk('.'))[2])

def slct_files(file_extension = '.txt'):
    """List all * files inside a folder.

    Args:
        file_path: the folder path as string
        file_extension: the extension youre lookin for
    Returns:
        A list.
    """
    ext_files = []
    for file in list_files():
        if file.endswith(file_extension):
            ext_files.append(file)
    return ext_files

def read_lines(file):
    """Return the lines of a textfile.

    Args:
        file: name of the textfile as string
    Returns:
        A list.
    """
    with open(file, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        f.close()
        return lines

def write_lines(file, lines):
    """Write a list of lines to a file.
    Args:
        file: name of the textfile as string
        lines: list of lines
    """
    with open(file, 'w', encoding = 'utf-8') as f:
        f.writelines(lines)
        f.close()

if __name__ == '__main__':
    print(f'Möchten sie die Dateien {slct_files()} wirklich verschlüsseln? y/n')
    if input('>>> ') == 'y':
        for file in slct_files():
            lines_e = []
            for line in read_lines(file):
                lines_e.append(cryptocode.encrypt(line, keyword) + '\n')
            write_lines(file, lines_e)
