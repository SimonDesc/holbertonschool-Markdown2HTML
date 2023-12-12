#!/usr/bin/python3
"""
Ce script est un outil de ligne de commande pour convertir un
fichier Markdown en fichier HTML.
"""
import sys
import os


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


def open_file(markdown_file):
    """
    The `open_file` function reads a markdown file and converts it into an
    HTML string, handling
    headers, lists, and other cases.

    :param markdown_file: The `markdown_file` parameter is a string that
    represents the file path of the
    Markdown file that you want to open and convert to HTML
    :return: a string containing the HTML representation of the contents
    of the markdown file.
    """

    html_str = ''
    current_buffer = []
    buffer_type = None

    def flush_buffer():
        # fait référence aux variables dans la fonction englobante
        nonlocal current_buffer, buffer_type, html_str
        if current_buffer:
            if buffer_type == 'unordered':
                html_str += handle_list(current_buffer)
            elif buffer_type == 'ordered':
                html_str += handle_ordered_list(current_buffer)
            elif buffer_type == 'paragraph':

                html_str += replace_line_p(current_buffer)
            current_buffer = []
            buffer_type = None

    with open(markdown_file) as f:
        for line in f:

            clean_line = line.strip()
            # if not clean_line:
            #     continue

            # Détecter le type de contenu et créer/vider les buffers
            if clean_line.startswith('#'):
                flush_buffer()
                html_str += replace_dieze(clean_line)
                continue

            if clean_line.startswith('-'):
                if buffer_type != 'unordered':
                    flush_buffer()
                    buffer_type = 'unordered'
                current_buffer.append(clean_line)
                continue

            if clean_line.startswith('*'):
                if buffer_type != 'ordered':
                    flush_buffer()
                    buffer_type = 'ordered'
                current_buffer.append(clean_line)
                continue

            if not clean_line.startswith(('#', '-', '*')):
                if clean_line:
                    if buffer_type != 'paragraph':
                        flush_buffer()
                        buffer_type = 'paragraph'
                    current_buffer.append(clean_line)
                else:
                    flush_buffer()

        flush_buffer()  # Pour traiter tout contenu restant

    return html_str


def handle_ordered_list(list_buffer):
    """
    The function "handle_ordered_list" takes a list of items and returns
    an HTML ordered list.

    :param list_buffer: The `list_buffer` parameter is a list that contains
    the items of the ordered
    list. Each item in the list represents a line of text that needs to be
    converted into an HTML list
    item
    :return: an HTML ordered list (ol) as a string.
    """
    html_list = "<ol>\n"
    for item in list_buffer:
        html_list += replace_list(item)
    html_list += "</ol>\n"
    return html_list


def handle_list(list_buffer):
    """
    The function "handle_list" takes a list as input and returns an HTML
    unordered list (ul) with each
    item in the list as a list item (li).

    :param list_buffer: The `list_buffer` parameter is a list of items that
    we want to convert into an
    HTML unordered list. Each item in the list will be a separate list item
    in the HTML output
    :return: an HTML unordered list (ul) with each item in the input
    list_buffer as a list item (li).
    """
    html_list = "<ul>\n"
    for item in list_buffer:
        html_list += replace_list(item)
    html_list += "</ul>\n"
    return html_list


def replace_list(line):
    """
    The `replace_list` function takes a line of text and returns it
    formatted as an HTML list item.

    :param line: The `line` parameter is a string that represents a
    line of text
    :return: a string that represents an HTML list item element. The content
    of the list item is
    obtained by removing the first character of the input line and any leading
    whitespace characters.
    The returned string is formatted as "<li>{content}</li>\n", where {content}
    is the extracted content
    from the input line.
    """
    content = line[1:].lstrip()
    return f"<li>{content}</li>\n"


def replace_line_p(paragraph):
    html_p = "<p>\n"

    for i, item in enumerate(paragraph):
        html_p += replace_line(item)
        if i < len(paragraph) - 1:
            html_p += '<br/>' + '\n'
    html_p += "</p>\n"
    return html_p


def replace_line(line):
    # Logique pour traiter les autres types de lignes
    return line + "\n"


def replace_dieze(line):
    """
    The function `replace_dieze` takes a line of text as input and replaces any
    leading hashtags with
    HTML header tags, returning the modified line.

    :param line: The `line` parameter is a string that represents a line
    of text
    :return: The function `replace_dieze` returns a modified version of
    the input
    `line` string. If the
    `line` starts with one or more "#" characters, it is considered a
    header line.
    The function removes
    the "#" characters and any leading spaces, and wraps the remaining content
    in HTML header tags
    `<h1>` to `<h6>` based on the number of "#" characters.
    """
    count = 0
    for character in line:
        if character == "#":
            count += 1
        else:
            break

    if count > 0:
        header_tag = f"<h{count}>"
        header_tag_end = f"</h{count}>"
        # Enlever les dièses et les espaces de début
        content = line[count:].lstrip()
        return f"{header_tag}{content}{header_tag_end}\n"
    else:
        return line + "\n"


def main():
    """
    The main function checks the user's input, transforms the content of
    a markdown file into HTML, and
    saves the HTML content into an output file.
    """
    # Check l'entrée de l'utilisateur
    markdown_file, output_file = check_input()

    # Transforme le contenu du fichier
    html_str = open_file(markdown_file)

    # Sauvegarde le fichier
    save_file(output_file, html_str)


if __name__ == "__main__":
    main()
