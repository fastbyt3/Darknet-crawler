import requests

# Set proxies for requests to use
proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

URL = "https://check.torproject.org/api/ip"

r = requests.get(URL, proxies=proxies)
print(r.text)