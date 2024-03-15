import requests
import os 

# take the input from the user and pre-process it
def process_input() -> str:
   query = str(input("Input (text): ")).strip()
   print(query)
   return query


def bing_web_search(input: str, exact: bool = True, num_results: int = 7):
   """Use Bing Web Search API to get the top 10 web results related to the query"""
   subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
   endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/v7.0/search"

   # Exact expression search
   query = f'"{input}"' if exact else input

   # Construct a request
   params = { 'q': query, 'mkt': 'en-US', 'count': num_results }
   headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

   # Call the API
   try:
      response = requests.get(endpoint, headers=headers, params=params) # default 10 results
      response.raise_for_status()
      search_results = response.json()
      return search_results
   except Exception as ex:
      raise ex


def bing_entity_search(input: str, exact: bool = True):
   """Use Bing Entity Search API to get more relevant query information"""
   subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
   endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/v7.0/entities"

   # Exact expression search
   query = f'"{input}"' if exact else input

   # Construct a request
   params = { 'q': query, 'mkt': 'en-US' }
   headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

   # Call the API
   try:
      response = requests.get(endpoint, headers=headers, params=params)
      response.raise_for_status()
      search_results = response.json()
      return search_results
   except Exception as ex:
      # print(search_results)
      raise ex

# using Bing Serach API, Bing Entity Search API, Crunchbase API
# using BeautifulSoup for web scraping
# using OpenaI GPT for summarizing the important information

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
