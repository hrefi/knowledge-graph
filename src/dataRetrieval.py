# using Bing Serach API, Bing Entity Search API, Crunchbase API
# using BeautifulSoup for web scraping
# using OpenaI GPT for summarizinggg the important information

# take the required input from the user and pre-process it
def processInput() -> str:
   query = str(input("Input (text): ")).strip()
   print(query)
   return query





# """Exact Search"""
# query = f'"{query}"'




# Preprocess Text - remove irrelevant sections, such as navigation menus or footers, using heuristics or HTML structure analysis
# Summarize the search information - 128k context window so might not need it - however, it might be helpful if it helps the LLM to be more precise


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
