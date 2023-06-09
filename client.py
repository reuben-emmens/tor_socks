'''This script demonstrates how to use Tor with Python to make requests over the Tor network.'''
import cProfile
import os
import pstats

import requests
from stem import Signal
from stem.control import Controller

def renew_tor_circuit():
    '''Renew the Tor circuit and generate a new IP address.'''
    # Access password as secret environment variable
    password = os.environ.get('TOR_PASSWORD')

    with Controller.from_port(port=9051) as controller: # type: ignore
        controller.authenticate(password=password)
        controller.signal(Signal.NEWNYM) # type: ignore # pylint: disable=no-member

def make_request(url):
    '''Make a request over the Tor network.'''
    renew_tor_circuit()

    timeout = 120

    proxy = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    response = requests.get(url, proxies=proxy, timeout=timeout)
    print(response.text)

def main():
    '''Entry point to the program'''
    url = 'https://checkip.amazonaws.com'
    cProfile.run(f'make_request("{url}")', 'profile_stats')

    stats = pstats.Stats('profile_stats')
    stats.strip_dirs()
    stats.sort_stats('cumulative')  # Sort by cumulative time
    stats.print_stats()

if __name__ == '__main__':
    main()
