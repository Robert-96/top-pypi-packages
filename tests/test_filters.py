import pytest

from scripts.build import format_number, format_download_count


@pytest.mark.parametrize(
    "number, expected", [
        (0, "0"),
        (5, "5"),
        (25, "25"),
        (100, "100"),
        (525, "525"),
        (2000, "2,000"),
        (2020, "2,020"),
        (3000000, "3,000,000"),
        (5100005, "5,100,005")
    ]
)
def test_format_number(number, expected):
    assert format_number(number) == expected


@pytest.mark.parametrize(
    "number, expected", [
        (5, "5"),
        (25, "25"),
        (100, "100"),
        (2_000, "2K"),
        (5_432, "5.43K"),
        (6_000_000, "6M"),
        (7_654_321, "7.65M"),
        (8_000_000_000, "8B"),
        (9_876_543_210, "9.88B")
    ]
)
def test_format_download_count(number, expected):
    assert format_download_count(number) == expected
