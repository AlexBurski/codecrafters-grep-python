import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    ends_with_anchor = False
    if pattern.endswith("$"):
        ends_with_anchor = True
        pattern = pattern[:-1]

    if pattern.startswith("^"):
        return string_search(
            pattern[1:], input_line, start_index=0, flag_endwith=ends_with_anchor
        )
    else:
        for i in range(len(input_line)):
            if string_search(
                pattern, input_line, start_index=i, flag_endwith=ends_with_anchor
            ):
                return True
        return False


def match_element(pattern, pattern_index, input_line, input_index):
    """
    Match a single element in the pattern at the given index.
    Returns:
        (success, pattern_consumed_length, input_consumed_length)
    """
    if pattern_index >= len(pattern) and input_index >= len(input_line):
        return False, 0, 0

    if pattern[pattern_index : pattern_index + 2] == r"\d":
        if not input_line[input_index].isdigit():
            return False, 0, 0
        return True, 2, 1
    elif pattern[pattern_index : pattern_index + 2] == r"\w":
        if not input_line[input_index].isalnum():
            return False, 0, 0
        return True, 2, 1

    elif pattern[pattern_index] == "[":
        closing_bracket_index = pattern.find("]", pattern_index)
        if closing_bracket_index == -1:
            raise ValueError("Unmatched '[' in pattern")

        char_set = pattern[pattern_index + 1 : closing_bracket_index]
        is_negated = char_set.startswith("^")

        if is_negated:
            char_set = char_set[1:]

        if (is_negated and input_line[input_index] in char_set) or (
            not is_negated and input_line[input_index] not in char_set
        ):
            return False, 0, 0

        return True, closing_bracket_index - pattern_index + 1, 1
    else:
        if not pattern[pattern_index] == input_line[input_index]:
            return False, 0, 0
        return True, 1, 1


def string_search(pattern, input_line, start_index, flag_endwith=False):
    pattern_index = 0
    input_index = start_index

    while pattern_index < len(pattern):
        # Check if we reached the end
        if input_index >= len(input_line):
            return False

        if pattern_index + 1 < len(pattern) and pattern[pattern_index + 1] == "+":
            success, element_length, _ = match_element(
                pattern, pattern_index, input_line, input_index
            )
            if not success:
                return False

            input_consumed = 0

            while input_index + input_consumed < len(input_line):
                success, _, len_input = match_element(
                    pattern, pattern_index, input_line, input_index + input_consumed
                )
                if success:
                    input_consumed += len_input
                else:
                    break

            if input_consumed == 0:
                return False

            pattern_index += element_length + 1
            input_index += input_consumed

        else:
            success, element_length, input_consumed = match_element(
                pattern, pattern_index, input_line, input_index
            )
            if not success:
                return False
            pattern_index += element_length
            input_index += input_consumed

    if flag_endwith:
        return input_index == len(input_line)
    else:
        return True


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
