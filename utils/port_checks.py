import socket
from contextlib import closing
import requests as r
import warnings

warnings.filterwarnings("ignore")


def is_port_open(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)
        return sock.connect_ex((host.strip(), port)) == 0


def is_url_valid(url, method='get'):
    response = getattr(r, method)(url, verify=False)
    return response.ok


if __name__ == "__main__":
    host = r"wp.pl"
    port = 443

    print(is_port_open(host, port))
    print(is_url_valid('https://{}:{}'.format(host, port)))
