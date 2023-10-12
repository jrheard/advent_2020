import itertools


def load_line_groups_from_file(filename: str) -> list[list[str]]:
    """Several AOC problems involve handling input files with groups of lines separated by an empty line, like this:

    ```
    zlim
    hlvb

    ejnypwcmsutbdkqf
    swfptbqucykmdn

    qgcmfhdspiywu
    csuihkqpydf
    icqasudphfy
    ```

    This function, when given the name of a file like that, will return a list of lists of strings like:
    [
        ['zlim', 'hlvb'],
        ['ejnypwcmsutbdkqf', 'swfptbqucykmdn'],
        ['qgcmfhdspiywu', 'csuihkqpydf', 'icqasudphfy'],
    ]
    """
    with open(filename) as f:
        lines = [line.strip() for line in f]

    result = []
    for is_an_empty_line, lines_since_last_empty_line in itertools.groupby(
        lines, key=lambda v: v == ""
    ):
        if is_an_empty_line:
            continue

        result.append(list(lines_since_last_empty_line))

    return result
