# using Bing Serach API, Bing Entity Search API, Crunchbase API
# using BeautifulSoup for web scraping
# using OpenaI GPT for summarizinggg the important information

import requests
from bs4 import BeautifulSoup

def extract_text(search_results):
   all_text = ""
   for result in search_results:
      url = result['link']
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      text = soup.get_text(strip=True) 
      all_text += " " + text
   return all_text
