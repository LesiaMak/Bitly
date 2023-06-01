import os
import requests
import argparse
from urllib.parse import urlparse
from environs import Env


def is_bitlink(token, link):
    headers = {
      'Authorization': 'Bearer {}'.format(token),
    }
    response = requests.get(
        'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(link),
        headers=headers
        )
    return response.ok


def shorten_link(token, link):
    headers = {
      'Authorization': 'Bearer {}'.format(token),
    }
    long_url = {"long_url": link}
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten', 
        headers=headers, 
        json=long_url
        )
    response.raise_for_status()
    bitlink = response.json()
    return bitlink['link']


def count_clicks(token, link):
    headers = {
      'Authorization': 'Bearer {}'.format(token),
    }
    params = {
      'unit': 'day',
      'units': '-1',
    }
    parsed_url = urlparse(link)
    erged_link = f"{parsed_url.netloc}{parsed_url.path}"
    response = requests.get(
        'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(merged_link), 
        headers=headers, 
        params=params
        )
    response.raise_for_status()
    number_clicks = response.json()
    return number_clicks['total_clicks']


def main():
    env = Env()
    env.read_env()
    bitly_token = env.str('BITLY_TOKEN')
    parser = argparse.ArgumentParser(description='Shorten links and count clicks')
    parser.add_argument('url', type=str, help='Input link')
    args = parser.parse_args()
    url = args.url
    print(url)
    if is_bitlink(bitly_token, url):
        try:
            print('Number clicks is ', count_clicks(bitly_token, url))
        except requests.exceptions.HTTPError:
            print('This link does not exist')
        else:
            try:
                print('Bitlink - ', shorten_link(bitly_token, url))
            except requests.exceptions.HTTPError:
                print('You have input unexisted url')    


if __name__ == '__main__':
    main()
