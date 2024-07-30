#!/usr/local/bin/python3
from sys import argv


def split_linewise(jon_code):
    lines = []
    for line in jon_code.split("."):
        lines.append(line.strip())

    return lines


def parse(line):
    tokens = []
    token = ""
    inside_quotes = ""
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

    if tokens[0] != "jon":
        raise Exception("statement does not begin with \"jon\"")

    match tokens[1]:
        case "says":
            return f"print('{tokens[2]}')"


def main():
    file = argv[0].split("/")[0] + "/" + argv[1]
    try:
        with open(file, 'r') as f:
            jon_code = f.read()
    except FileNotFoundError:
        print(file, "does not exist...")
        exit()

    lines = split_linewise(jon_code)

    out = []

    for line in lines:
        out.append(parse(line))

    print(out)

    print('~'*10)
    for expression in out:
        exec(expression)


if __name__ == "__main__":
    main()
