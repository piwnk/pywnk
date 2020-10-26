import socket
from contextlib import closing
import requests as r
import warnings

warnings.filterwarnings("ignore")


def is_port_open(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


def is_valid(url, method='post'):
    response = getattr(r, method)(url, verify=False)
    return response.ok


if __name__ == "__main__":
    host = r"wp.pl"
    port = 443
    url = 'https://{}:{}'.format(host, port)

    print(is_port_open(host, port))
    print(is_valid(url))
