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

def run(argv=[], *a, **kv):    
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    totalLinks = 0
       
    if "-d" in opts:
        logging.info(f"Scraping links from {args[0]}")
        links = scrapeLinks(args[0])
        # if links:
        #     totalLinks += len(links)
        #     writeToFile(links)
    elif "-f" in opts:
        with open(args[0]) as f:
            inp = f.readlines()
            for inplink in inp:
                inplink = inplink.strip()
                links = scrapeLinks(inplink)
                if links:
                    totalLinks += len(links)
                    writeToFile(links)
    else:
        links = scrapeLinks("http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/")
        totalLinks += len(links)
        writeToFile(links)
    
    if "-r" in opts:
        noOfRecursions = args[1]
        with open("scraped-links.txt", mode='r') as f:
            for _ in range(int(noOfRecursions)):
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    # print(line.strip())
                    logging.info(f"Scraping links from {line}")
                    links = scrapeLinks(line)
                    if links:
                        totalLinks += len(links)
                        writeToFile(links)

# Scrape all links from passed URL
def scrapeLinks(URL):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        res = requests.get(URL, headers=headers)
    except ConnectionError:
        logging.info(f"This site {URL} is not reachable")
        return None
    
    soup = BeautifulSoup(res.content, 'html.parser')

    title = (soup.title).string
    logging.info(f"site tile: {title}")

    print(soup.prettify())
    
    links = [link.get('href') for link in soup.find_all('a')]
    links = list(filter(None, links))

    # Remove all "non-onion" sites:
    for link in links:
        if "onion" not in link:
            links.remove(link)

    print(links)

    numOfLinks = len(links)
    logging.info(f"Number of links scraped: {numOfLinks}")

    return links

def writeToFile(data):
    f = open("scraped-links.txt", "a")
    for i in data :
        f.write(i)
        f.write('\n')
    f.close()

if __name__ == '__main__':
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
    socket.socket = socks.socksocket
    socket.getaddrinfo = getaddrinfo

    setupLogger(logging.INFO)

    run()
    
    logging.info("Finished!")