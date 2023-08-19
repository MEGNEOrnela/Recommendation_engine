import asyncio
import json
from collections import defaultdict
from itertools import chain
from turtle import title
from typing import List, Optional, Tuple, TypedDict

import aiohttp
from bs4 import BeautifulSoup
import requests

"""
This file scrapes french african songs + lyrics from "https://afrikalyrics.com/top-lyrics"
"""

# URL = "https://afrikalyrics.com/language/French"
URL = "https://afrikalyrics.com/top-lyrics"


async def get_author_title_and_lyrics_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            # Extract all titles and links
            items = soup.select('.item-info')
            title_and_urls = []
            for item in items:
                item_title = item.select_one('.item-title a')['title']
                item_author = item.select_one('.item-author a').text.strip()
                item_link = item.select_one('.item-title a')['href']
                title_and_urls.append([item_author,item_title,item_link])

            return title_and_urls

async def get_lyrics_from_lyrics_url(lyric_url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(lyric_url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Find all the <span> tags with the inline style "font-size:18px" which appears to contain the lyrics
            lyrics_spans = soup.find_all('span', style='font-size:18px')

            # Extract the text representing the lyrics from each <span> tag
            lyrics = [span.get_text(strip=True) for span in lyrics_spans]

            # Join all the lyrics together into a single string (if needed)
            text = '\n'.join(lyrics)
            return text



async def main():
    data = await get_author_title_and_lyrics_url(URL)
    result = defaultdict(list)
    for author_name, title,lyrics_url in data:
        lyrics = await get_lyrics_from_lyrics_url(lyrics_url)
        result[author_name].append({"title":title,"text":lyrics})

    with open("data/lyrics.json", "w") as f:
        json.dump(result, f)



if __name__ == "__main__":
    asyncio.run(main())