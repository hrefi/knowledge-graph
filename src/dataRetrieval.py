from openai import OpenAI
import requests
import os 

client = OpenAI()

# take the input from the user and pre-process it
def process_input() -> str:
   query = str(input("Input (text): ")).strip()
   print(query)
   return query


def bing_web_search(input: str, exact: bool = True, num_results: int = 7):
   """Perform a web search using Bing Web Search API
    
   Parameters:
      input (str): The search query.
      exact (bool): Whether to perform an exact search. Defaults to True.
      num_results (int): Number of search results to return. Defaults to 7.
   
   Returns:
      dict: The search results returned by Bing Web Search API.
   """
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
   """Use Bing Entity Search API to get more relevant query information
    
   Parameters:
      input (str): The search query.
      exact (bool): Whether to perform an exact search. Defaults to True.
   
   Returns:
      dict: The search results returned by Bing Entity Search API.
   """
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


def generate_additional_data(query: str, model: str = "gpt-3.5-turbo"):
   """Generate additional data about the query using OpenAI's GPT model.

   Parameters:
      query (str): The search query.
      model (str): Model to use, defaults to "gpt-3.5-turbo".

   Returns:
      str: The generated text.
   """
   # Prompt:
   # Identify important, specific entities related to {query}.
   # These entities could include specific people, companies, locations, universities, professional affiliations, etc., but not attributes of {query}. 
   # Extract the relevant relationships between {query} and the entities you identified. 
   # You must return an empty response if information isn't available.
   msg_list = f"""Identify important, specific entities related to {query}. These entities could include specific people, companies, locations, universities, professional affiliations, etc., but not attributes of {query}. Extract the relevant relationships between {query} and the entities you identified.\nYou must return an empty response if information isn't available."""

   completion = client.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": msg_list}]
   )

   return completion.choices[0].message.content


# import requests
# from bs4 import BeautifulSoup

# def extract_text(search_results):
#    """Extract text from web page URLs contained in search results.
   
#    Parameters:
#       search_results (list): A list of search result items with 'link' keys.
   
#    Returns:
#       str: Concatenated text from all web pages.
#    """
#    all_text = ""
#    for result in search_results:
#       url = result['link']
#       response = requests.get(url)
#       soup = BeautifulSoup(response.content, 'html.parser')
#       text = soup.get_text(strip=True) 
#       all_text += " " + text
#    return all_text
