#!/usr/bin/python3
"""
Ce script est un outil de ligne de commande pour convertir un
fichier Markdown en fichier HTML.
"""
import sys
import os


def replace_dieze(markdown_array):
    """
    The `replace_dieze` function takes in an array of strings in Markdown
    format and replaces the '#'
    symbols at the beginning of each string with the corresponding
    HTML heading tags.

    :param markdown_array: The `markdown_array` parameter is expected to
    be a list of strings, where
    each string represents a line of markdown text
    :return: a string that has replaced the '#' symbols in the input
    markdown_array with the
    corresponding HTML heading tags.
    """
    new_array = []
    dict_dieze = {
        "1": "<h1>",
        "2": "<h2>",
        "3": "<h3>",
        "4": "<h4>",
        "5": "<h5>",
        "6": "<h6>",
    }
    dict_dieze_end = {
        "1": "</h1>",
        "2": "</h2>",
        "3": "</h3>",
        "4": "</h4>",
        "5": "</h5>",
        "6": "</h6>",
    }
    for string in markdown_array:
        count = 0
        for character in string:
            if character == "#":
                count += 1
            else:
                break
        if count > 0:
            new_array.append(dict_dieze[str(count)])
            old_string = string.replace("#", "")
            new_array.append(old_string.lstrip())
            new_array.append(dict_dieze_end[str(count)])
            new_array.append("\n")

    return "".join(new_array)


def open_file(markdown_file):
    """
    The function `open_file` reads a markdown file and returns its contents as
    an array of strings.

    :param markdown_file: The parameter `markdown_file` is a string that
    represents the file path of the
    markdown file you want to open and read
    :return: The function `open_file` returns an array of strings, where
    each string represents a line
    from the markdown file.
    """
    markdown_array = []
    with open(markdown_file) as f:
        for line in f:
            # créé un tableau des strings sans \n
            markdown_array.append(line.strip())
    return markdown_array


def save_file(output_file, html_format):
    """
    The function `save_file` saves the provided `html_format` to
    the specified `output_file`.

    :param output_file: The output_file parameter is the name or
    path of the file where you want to save
    the HTML content
    :param html_format: The `html_format` parameter is a string that
    represents the HTML content that
    you want to save to a file
    """
    with open(output_file, "w") as f:
        f.write(html_format)


def check_input():
    """
    The function `check_input()` checks if the correct number of command
    line arguments are provided and
    if the input markdown file exists. It returns the names of the
    markdown file and the output file.
    :return: the values of the variables `markdown_file` and `output_file`.
    """
    if sys.argv is False or len(sys.argv) < 3 or len(sys.argv) > 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(markdown_file):
        sys.stderr.write("Missing " + markdown_file + "\n")
        exit(1)

    return markdown_file, output_file


def main():
    # Check l'entrée de l'utilisateur
    markdown_file, output_file = check_input()

    # Transforme le contenu du fichier en array
    markdown_array = open_file(markdown_file)

    # Transforme les # en titre html
    html_title_str = replace_dieze(markdown_array)

    # Sauvegarde le fichier
    save_file(output_file, html_title_str)


if __name__ == "__main__":
    main()
