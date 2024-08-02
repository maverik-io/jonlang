#!/usr/local/bin/python3
import os
from sys import argv
import subprocess
import colorama


class IDontUnderstand(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def split_linewise(jon_code):
    lines = []
    line = ''
    inside_quotes = False

    for c in jon_code:
        if c == '"':
            inside_quotes = not inside_quotes
            line += '"'
        elif c == '!' and not inside_quotes:
            line = line.strip()
            lines.append(line)
            line = ''
        else:
            line += c

    if line.strip():
        lines.append(line.strip())

    print(f"{lines=}")

    return lines


def parse(line):
    tokens = []
    token = ""
    inside_quotes = False

    for c in line:
        if c == '"':
            inside_quotes = not inside_quotes
        elif c == " " and not inside_quotes:
            if token != "":
                tokens.append(token)
            token = ""
        else:
            token += c

    tokens.append(token)

    if tokens[0] != "jon,":
        raise IDontUnderstand("statement does not begin with \"jon,\"")

    print(f"{tokens=}")

    return tokens


def to_python(tokens):
    match tokens[1]:
        case "say":
            if len(tokens) == 3:
                return f"print('{tokens[2]}')\n"

            elif len(tokens) > 3:
                if tokens[3] != 'and' or tokens[4] != "read":
                    raise IDontUnderstand

                match tokens[5]:
                    case "into":
                        return f"{tokens[6]} = eval(input('{tokens[2]}'))\n"
                    case "aloud":
                        return f"print('{tokens[2]}', {tokens[6]})\n"

        case "remember":
            if tokens[2] != 'that':
                raise IDontUnderstand("did you mean `remember that` ?")

            match tokens[4]:
                case "is":
                    return f"{tokens[3]} = {tokens[5]}\n"

                case "will":
                    if tokens[5] != 'be':
                        raise IDontUnderstand("did you mean `will be` ?")

                    first_val = tokens[6]
                    operator = ''
                    match tokens[7]:
                        case "plus":
                            operator = "+"
                        case "minus":
                            operator = "-"
                        case "times":
                            operator = "*"
                        case "by":
                            operator = "/"

                    second_val = tokens[8]

                    return \
                        f"{tokens[3]} = {first_val} {operator} {second_val}\n"

    return ''


def main():
    jon_awake = False
    file = argv[0].split("/")[0] + "/" + argv[1]
    try:
        with open(file, 'r') as f:
            jon_code = f.read()
    except FileNotFoundError:
        print(file, "does not exist...")
        exit()

    lines = split_linewise(jon_code)

    tokens_list = []
    for line in lines:
        if line == "hi, jon":
            jon_awake = True
        elif line == "bye, jon":
            jon_awake = False

        elif jon_awake:
            tokens_list.append(parse(line))

    out = []
    for tokens in tokens_list:
        out.append(to_python(tokens))
    print(out)

    print('~'*10)

    with open('output.py', 'w') as f:
        f.writelines(out)

    subprocess.run(["python3", "output.py"])
    os.remove("output.py")


if __name__ == "__main__":
    try:
        main()
    except IDontUnderstand as e:
        print(e)
