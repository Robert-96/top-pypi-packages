"""A collection of custom Jinja2 filters."""

from decimal import Decimal, ROUND_DOWN


def format_number(number):
    """Format a number to more readable string.

    Args:
        str: A string containing the formatted number.

    Example:
        >>> format_number(321)
        '321'

        >>> format_number(5_432)
        '5,432'

        >>> format_number(7_654_321)
        '7,654,321'

        >>> format_number(9_876_543_210)
        '9,876,543,210'

    """

    return '{:,}'.format(number)


def format_download_count(number):
    """Format a number to more readable download count.

    Returns:
        str: A string containing the formatted number.

    Examples:
        >>> format_download_count(321)
        '321'

        >>> format_download_count(5_000)
        '5K'

        >>> format_download_count(5_432)
        '5.43K'

        >>> format_download_count(7_654_321)
        '7.65M'

        >>> format_download_count(9_876_543_210)
        '9.87B'

    """

    number_map = [
        (1_000_000_000, 'B'),
        (1_000_000, 'M'),
        (1_000, 'K'),
    ]

    for value, letter in number_map:
        if number < value:
            continue

        return '{}{}'.format(Decimal(number / value).quantize(Decimal('.01'), rounding=ROUND_DOWN).normalize(), letter)

    return str(number)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
