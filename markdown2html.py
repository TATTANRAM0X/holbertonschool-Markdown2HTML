#!/usr/bin/python3
"""Script markdown2html.py that takes an argument 2 strings"""
import sys
import os
import hashlib


def headings(line, html):
    """Function that parses the Headings Markdown syntax to generate HTML."""
    hash = txt = ''
    for character in line:
        "Number of hash"
        if character == '#':
            hash += character
        "Text without numerals"
        if character != '#':
            txt += character

    "Write in html file"
    with open(html, 'a') as f:
        if len(character) > 0 and len(hash) > 0:
            f.write("<h{len_h}>{txt}</h{len_h}>\n".format(
                len_h=len(hash), txt=txt[1:-1]
                ))


def reded_list(line, html):
    """Function that parses unordered listing syntax for generating HTML"""
    li = txt = ''
    "Case unordered list"
    if line[0] == '-':
        for character in line:
            "Number of li"
            if character == '-':
                li += character
            "Text without numerals"
            if character != '-':
                txt += character

        if len(li) > 0 and len(txt) > 0:
            with open(html, 'a') as f:
                "Write in html file"
                f.write("<li>{txt}</li>\n".format(txt=txt[1:-1]))

    "Case ordered list"
    if line[0] == '*':
        for character in line:
            "Number of li"
            if character == '*':
                li += character
            "Text without numerals"
            if character != '*':
                txt += character

        if len(li) > 0 and len(txt) > 0:
            with open(html, 'a') as f:
                "Write in html file"
                f.write("<li>{txt}</li>\n".format(txt=txt[1:-1]))


def bold(line):
    """Bold in the case"""
    asterisk = closed_stsk = 0
    underscore = closed_under = 0
    new_line = ''
    for i in range(len(line)):
        try:
            "Case Asterisk"
            if line[i] == '*' and line[i+1] == '*':
                asterisk += 1
                closed_stsk += 1
            if asterisk == 1:
                new_line += '<b>'
                asterisk /= 2
            if closed_stsk == 2:
                new_line += '</b>'
                asterisk = closed_stsk = 0

            "Case underscore"
            if line[i] == '_' and line[i+1] == '_':
                underscore += 1
                closed_under += 1
            if underscore == 1:
                new_line += '<em>'
                underscore /= 2
            if closed_under == 2:
                new_line += '</em>'
                underscore = closed_under = 0

            if line[i] != '*' and line[i] != '_' or line[i] == ' ' or\
                (line[i] == '*' and line[i+1] != '*' and line[i-1] != '*')\
                    or (line[i] == '_' and line[i+1] != '_' and
                        line[i-1] != '_'):
                new_line += line[i]

        except IndexError:
            i = len(line) - 1
    return new_line


def remove_c(line):
    "Function that remove the 'c' or 'C'"
    li = ne = ''
    c = 0
    for i in range(len(line)):
        try:
            if line[i] == '(' and line[i+1] == '(':
                c = 1
                i += 3
            if line[i] == ')' and line[i+1] == ')':
                c = 0
            if c == 1 and line[i] != '(' and line[i] != ')' and\
                    line[i] != 'c' and line[i] != 'C':
                li += line[i]
            if c == 0:
                li += ''
        except IndexError:
            i = len(line) - 1

    c = 0
    for i in range(len(line)):
        try:
            if line[i] == '(' and line[i+1] == '(':
                ne += li[1:]
                c = 1
            if c == 1:
                i += len(li) + 3
            if line[i] != '(' and line[i+1] != '(' and line[i] != ')'\
                    and line[i+1] != ')' or line[i] == ' ' or line[i] == '_':
                ne += line[i]
        except IndexError:
            i = len(line) - 1
    ne += '\n'
    return ne


def md5(line):
    "Function that convert a string in md5"
    li = ne = ''
    c = 0
    for i in range(len(line)):
        try:
            if line[i] == '[' and line[i+1] == '[':
                c = 1
            if line[i] == ']' and line[i+1] == ']':
                c = 0
            if c == 1 and line[i] != '[' and line[i] != ']':
                li += line[i]
            if c == 0:
                li += ''
        except IndexError:
            i = len(line) - 1

    c = 0
    md5 = hashlib.md5(li.encode('utf-8')).hexdigest()
    for i in range(len(line)):
        try:
            if line[i] == '[' and line[i+1] == '[':
                ne += md5
                c = 1
            if c == 1:
                i += len(li) + 2
            if line[i] != '[' and line[i+1] != '[' and line[i] != ']' and\
                    line[i+1] != ']' or line[i] == ' ' or line[i] == '_':
                ne += line[i]
        except IndexError:
            i = len(line) - 1
    ne += '\n'

    return ne


def switch(lines, html):
    """Switch in the case"""
    ul = closed_ul = ol = closed_ol = 0
    p = closed_p = br = 0
    lines = [(bold(remove_c(md5(line)))) for line in lines]
    for i in range(len(lines)):
        "Case headings"
        if lines[i][0] == '#':
            headings(lines[i], html)

        "Case unordered list"
        if lines[i][0] == '-':
            if i > 0:
                try:
                    if lines[i - 1][0] != '-' or lines[i + 1][0] != '-':
                        ul = 0
                    if lines[i + 1] == '\n':
                        ul = 1
                    if lines[i + 1][0] != '-':
                        closed_ul = 1
                except IndexError:
                    i = len(lines) - 1
            if ul == 0:
                with open(html, 'a') as f:
                    "Write in html file"
                    f.write("<ul>\n")
            reded_list(lines[i], html)
            if closed_ul == 1:
                with open(html, 'a') as f:
                    "Write in html file"
                    f.write("</ul>\n")
            ul = 1
            closed_ul = 0

        "Case ordered list"
        if lines[i][0] == '*':
            if i > 0:
                try:
                    if lines[i - 1][0] != '*' or lines[i + 1][0] != '*':
                        ol = 0
                    if lines[i + 1] == '\n':
                        ol = 1
                    if lines[i + 1][0] != '*':
                        closed_ol = 1
                except IndexError:
                    i = len(lines) - 1
            if ol == 0:
                with open(html, 'a') as f:
                    "Write in html file"
                    f.write("<ol>\n")
            reded_list(lines[i], html)
            if closed_ol == 1:
                with open(html, 'a') as f:
                    "Write in html file"
                    f.write("</ol>\n")
            ol = 1
            closed_ol = 0

        "Case paraghap/text"
        if lines[i][0] != '-' and lines[i][0] != '*' and lines[i][0] != '#':
            with open(html, 'a') as f:
                "Write in html file"
                try:
                    if i > 0:
                        if lines[i-1] == '\n':
                            p = 0
                    if lines[i+1] == '\n':
                        closed_p = 1
                    if lines[i+1][0] != '\n':
                        br = 1

                except IndexError:
                    i = len(lines) - 1
                if lines[i][0] != '\n':
                    if p == 0:
                        f.write("<p>\n")
                    f.write("{txt}".format(txt=lines[i]))
                    if br == 1:
                        f.write("<br/>\n")
                    if closed_p == 1:
                        f.write("</p>\n")
                p = 1
                closed_p = br = 0

    with open(html, 'a') as f:
        "Case unordered list"
        if lines[i][0] == '-':
            "Write in html file"
            f.write("</ul>\n")

        "Case ordered list"
        if lines[i][0] == '*':
            "Write in html file"
            f.write("</ol>\n")

        "Case paraghap/text"
        if lines[i][0] != '-' and lines[i][0] != '*' and lines[i][0] != '#':
            "Write in html file"
            f.write("</p>\n")


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args[1]):
        print("Missing {}".format(args[1]), file=sys.stderr)
        sys.exit(1)

    "Read markdown file"
    with open(args[1]) as f:
        lines = f.readlines()

    switch(lines, args[2])

    sys.exit(0)
