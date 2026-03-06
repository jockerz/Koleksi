#!/usr/bin/python3
import argparse

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

URL = 'https://www.kamusbatak.com'
NOT_FOUND_TEXT = '404'

http = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) '\
                  'Gecko/20100101 Firefox/78.0'
    }


def do_request(url_args: str, is_verbose: bool = False):
    url = f"{URL}/{url_args['bahasa']}/{url_args['teks']}.html"
    if is_verbose:
        print(f"Accessing url={url}")
    try:
        resp = http.post(url, params=url_args, headers=HEADERS)
        if is_verbose:
            print(f'  status code: {resp.status_code}')
        resp.raise_for_status()
        return resp.text
    except ConnectionError:
        print(" Connection failed")


def _process(elem_panel):
    strong = elem_panel.find('strong')
    italic = elem_panel.find_all('i')
    if strong:
        print(f' ▶️ {strong.text.strip()}')
    elif elem_panel.string:
        print(f' ▶️ {elem_panel.string.strip()}')
    
    for item in italic:
        print(f'   {item.text.strip()}')


def parse_html(html_text, is_verbose):
    soup = BeautifulSoup(html_text, 'html.parser')
    # panels = soup.find_all('div', class_='panel panel-default')
    panels = soup.find_all('div', class_='panel-body')

    proceed_one = False
    for panel in panels:
        #panel = panel.div
        if not panel.text:
            continue
        elif proceed_one is False:
            proceed_one = True
            for line in panel.text.strip().split('\n'):
                line = line.strip()
                print(f' ◼️ {line}')
        else:
            _process(panel)


def main():
    parser = argparse.ArgumentParser(
        description='Kamus Bahasa Batak - Indonesia dan sebaliknya')
    parser.add_argument('words', metavar='Word(s)', action="store", nargs="+",
                        help='Kata / kalimat yang ingin di terjemahkan')
    parser.add_argument('-i', action='store_true', default=False, dest='reverse',
                        help="Bahasa Indonesia - Batak")
    parser.add_argument('-v', action='store_true', default=False, dest='verbose')

    args = vars(parser.parse_args())

    bahasa = 'indonesia' if not args.get('reverse') else 'batak'

    if isinstance(args['words'], list):
        text = ' '.join(args['words'])
    else:
        text = args['words']
    url_args = {
        'teks': text, 'bahasa': bahasa,
        'submit': 'LIHAT HASIL TERJEMAHAN'
    }
    is_verbose = args['verbose']

    html = do_request(url_args, is_verbose)
    if html is None:
        return

    if NOT_FOUND_TEXT in html:
        print(f' {NOT_FOUND_TEXT}')
    else:
        result = parse_html(html, is_verbose)


if __name__ == '__main__':
    main()


