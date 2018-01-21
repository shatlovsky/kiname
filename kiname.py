#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import re
import sys

class imdb2filename:
    def __init__(self, url, ext):
        self.url = url
        self.ext = ext if ext is not None else ''

    def fetch_and_parse(self):
        req = urllib.request.Request(self.url)
        req.add_header('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3205.0 Safari/537.36")
        req.add_header('Accept-Language', 'en-US,en;q=0.8,pt;q=0.6')
        fn = ""
        with urllib.request.urlopen(req) as response:
            self.page = response.read()
            self.parse()

    def parse(self):
        soup = BeautifulSoup(self.page, 'html.parser')
        title_block = soup.find("div", class_="title_wrapper")
        self.year = title_block.h1.a.text
        self.title = re.search('^<[^<>]+>([^<>]+).<', str(title_block.h1)).group(1)
        original_title_block = title_block.find('div',class_='originalTitle')
        match = re.search('^<[^<>]+>([^<>]+)<', str(original_title_block))
        self.original_title = match.group(1) if match else None

    def make_file_name(self):
        self.fetch_and_parse()
        title = self.original_title if self.original_title is not None else self.title 
        fn = '"%s (%s).%s"' % (title, self.year, self.ext) 
        return fn

def main():
    if len(sys.argv) == 3:
        url = sys.argv[1]
        ext = sys.argv[2]
        print("url:%s ext:%s" % (url, ext))
        k = imdb2filename(url, ext)
        fn = k.make_file_name()
        print("Plex recommended file name:\n%s" % fn)
    else:
        print(len(sys.argv))
        print("Usage:\n\t%s URL extension" % (sys.argv[0]))
    

if __name__ == "__main__":
    main()

