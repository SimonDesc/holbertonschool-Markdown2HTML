#!/usr/bin/python3
"""
Ce script est un outil de ligne de commande pour convertir un
fichier Markdown en fichier HTML.
Il prend deux arguments : le fichier source en Markdown et
le nom du fichier de sortie HTML.
Le script vérifie la validité des arguments et l'existence du fichier source
avant de procéder à la conversion.
"""
import sys
import os


if __name__ == "__main__":
    if (sys.argv is False or len(sys.argv) < 3 or len(sys.argv) > 3):
        sys.stderr.write('Usage: ./markdown2html.py README.md README.html \n')
        exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(markdown_file):
        sys.stderr.write('Missing ' + markdown_file + '\n')
        exit(1)
