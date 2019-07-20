"""Swear updating module."""
import re
import string
from typing import List
from urllib.request import Request, urlopen


def generate_swear_file(filename: str) -> None:
    """
    Collect fresh list of bad language and save it to a file.

    The words are fetched from https://www.noswearing.com/dictionary
    """
    swear_list: List[str] = []
    urls = [f'https://www.noswearing.com/dictionary/{letter}' for letter in string.ascii_lowercase]

    for url in urls:
        # set Firefox User-Agent header to don't be blocked be the server
        request = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 Firefox/68.0'})
        with urlopen(request) as response:
            html = response.read().decode()
            matches = re.findall(r'name="(\w+)"><[/]a><b>', html)
            swear_list += matches

    with open(filename, 'w+', encoding='utf-8') as file:
        file.write('\n'.join(swear_list))
