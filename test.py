import socks
import socket
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

