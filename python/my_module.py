import requests
from lxml import html

def count_words_at_url(url):
    resp = requests.get(url, verify=False)
    return len(resp.text.split())

def download_page(url):
    print(url)
    resp = requests.get(url, verify=False)    
    with open("content.txt",'wb') as content_file:
        content_file.write(resp.content)
    content_file.close()
    return

def count_links():
    with open("page.txt",'r') as content_file:
        content = content_file.read()
        webpage = html.fromstring(content)
        print(webpage.xpath('//a/@href'))
    return

