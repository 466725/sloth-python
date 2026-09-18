"""Simple ASCII uppercase conversion utility."""


def upper(word: str) -> str:
    """Convert lowercase ASCII letters in ``word`` to uppercase.

    >>> upper("wow")
    'WOW'
    >>> upper("Hello")
    'HELLO'
    >>> upper("WHAT")
    'WHAT'
    >>> upper("wh[]32")
    'WH[]32'
    """

    result_chars: list[str] = []
    a_ascii = ord('a')
    z_ascii = ord('z')
    for char in word:
        if a_ascii <= ord(char) <= z_ascii:  # 'a'..'z'
            result_chars.append(chr(ord(char) - 32))
        else:
            result_chars.append(char)
    return "".join(result_chars)


if __name__ == "__main__":
    print(upper("Hello world! "))
    from doctest import testmod

    testmod()
