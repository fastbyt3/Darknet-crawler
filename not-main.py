import logging
import requests
import socks
import socket
import sys
from bs4 import BeautifulSoup
from requests import ConnectionError
from urllib.request import urlopen

# Setup tor proxy
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

# Setup logger
def setupLogger(level=logging.DEBUG):
    logging.basicConfig(
        filename="just-a-log.log", 
        filemode="w", 
        level=level,
        format='[+] %(message)s'
    )

# Scrape all links from passed URL
def scrapeLinks(URL):
    # logging.info(f"Sending a GET request to specified site: {URL}")
    try:
        res = requests.get(URL)
    except ConnectionError:
        logging.info(f"This site {URL} is not reachable")
        return None
    soup = BeautifulSoup(res.content, 'html.parser')
    title = (soup.title).string
    logging.info(f"scraped for links: {title}")

    # print(soup.prettify())
    
    links = [link.get('href') for link in soup.find_all('a')]
    links = list(filter(None, links))

    # Remove all "non-onion" sites:
    for link in links:
        if "onion" not in link:
            links.remove(link)
        # re = regex.compile('')

    return links

def writeToFile(data):
    f = open("scraped-links.txt", "a")
    for i in data :
        f.write(i)
        f.write('\n')
    f.close()

if __name__ == '__main__':
    # Set up tor socket
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
    socket.socket = socks.socksocket
    socket.getaddrinfo = getaddrinfo
    # Logger
    setupLogger(logging.INFO)
    # Provide tor link to scrape for other links 
    links = scrapeLinks("http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/")
    writeToFile(links)
    # for i in links:
    #     links = scrapeLinks(i)
    #     if links:
    #         writeToFile(links)
    logging.info("Finished!")