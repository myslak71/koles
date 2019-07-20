"""Swear updating module."""
import string

from requests_html import HTMLSession


def generate_swear_file(filename: str) -> None:
    """Collect fresh list of bad language and save it to a file."""
    swear_list = []
    urls = [f'https://www.noswearing.com/dictionary/{letter}' for letter in string.ascii_lowercase]
    session = HTMLSession()

    for url in urls:
        response = session.get(url)
        links = response.html.find('[width="650"] [name]')
        for link in links:
            swear_list.append(link.attrs["name"])

    with open(filename, 'w+', encoding='utf-8') as file:
        file.write('\n'.join(swear_list))
