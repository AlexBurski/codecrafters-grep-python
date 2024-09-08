import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern == r'\d':
        return any(char.isdigit() for char in input_line)
    elif pattern == r'\w':
        return any(char.isalnum() for char in input_line)
    elif "[" in pattern:
        return positive_char_from_group(pattern, input_line)
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")

def positive_char_from_group(group, input_line):
    for char in group:
        if char not in ("[", "]"):
            if char in input_line:
                return True

    return False

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
