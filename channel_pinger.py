from requests_html import HTMLSession 
from bs4 import BeautifulSoup
# from bs4 import BeautifulSoup as bs
import requests

# DANGER: This will download chromium(109MB)
channel_url = "https://www.youtube.com/c/Ludwigahgren"

# r = requests.get(channel_url)
# page = (r.text)
# print(r.text)
# soup=bs(page,'html.parser')

# f=soup.find('span')
# print(f['aria-label'])

print('starting sesh')
session = HTMLSession()
response = session.get(channel_url)
response.html.render()
print(response.html.links)