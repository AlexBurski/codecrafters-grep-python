import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    for i in range(len(input_line)):
        if recursive_search(pattern, input_line[i:], start_index = i):
            return True
    return False
def positive_char_from_group(group, input_line):
    start_index = group.find("[")
    end_index = group.find("]")

    if start_index == -1 or end_index == -1 or start_index > end_index:
        raise ValueError("Pattern must contain characters between '[' and ']'")
    character_set = set(group[start_index + 1: end_index])
    input_line_set = set(input_line)

    if start_index + 1 == group.find("^"):
        return not bool(character_set & input_line_set)

    return bool(character_set & input_line_set)

def recursive_search(pattern, input_line, start_index):
    pattern_index = 0
    input_index = start_index

    while pattern_index < len(pattern) and input_index < len(input_line):
        if pattern[pattern_index:pattern_index + 2] == r"\d":
            if not input_line[input_index].isdigit():
                return False
            pattern_index += 2
            input_index += 1
        elif pattern[pattern_index:pattern_index + 2] == r"\w":
            if not input_line[input_index].isalnum():
                return False
            pattern_index += 2
            input_index += 1

        elif pattern[pattern_index] == '[':
            closing_bracket_index = pattern.find(']', pattern_index)
            if closing_bracket_index == -1:
                raise ValueError("Unmatched '[' in pattern")

            char_set = pattern[pattern_index + 1:closing_bracket_index]
            is_negated = char_set.startswith('^')

            if is_negated:
                char_set = char_set[1:]

            if (is_negated and input_line[input_index] in char_set) or (
                    not is_negated and input_line[input_index] not in char_set):
                return False

            pattern_index = closing_bracket_index + 1
            input_index += 1

        elif pattern[pattern_index] == input_line[input_index]:
            pattern_index += 1
            input_index += 1
        else:
            return False

    return pattern_index == len(pattern)

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)


    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
