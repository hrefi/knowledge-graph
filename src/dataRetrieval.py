from openai import OpenAI
import requests
import os 


# TODO: Future Development
# - Receive additional input for topic / type of the relationships wanted, # e.g., only show investments, locations, co-workers, etc.
# - Investigate other search APIs or knowledge bases to diversify results, # e.g., Google Search API, SerpApi, Crunchbase API
# - Implement web page scraping to get more information and use OpenAI’s text embeddings for searching


client = OpenAI()

# take the input from the user and pre-process it
def process_input() -> str:
   query = str(input("Input (text): ")).strip()
   print(query)
   return query


def retrieve_data(query: str, num_results: int = 7, model: str = "gpt-3.5-turbo"):
   """Retrieve information about the query. Uses Bing Web Search, Bing Entity Search, OpenAI GPT model
    
   Parameters:
      query (str): The search query.
      num_results (int): Number of search results to return. Defaults to 7.
      model (str): Model to use, defaults to "gpt-3.5-turbo".
   
   Returns:
      str: The information collected."""
   # Retrieve web resources using Bing and combine the results in a single string
   bing_entity_search_results = bing_entity_search(query)
   bing_web_search_results = bing_web_search(query, num_results=num_results)
   combined_results = []

   # Retrieve entity information if any
   if "entities" in bing_entity_search_results:
      for entity in bing_entity_search_results["entities"]["value"]:
         combined_results.append(str(entity['description']))

   # Retrieve top web search snippets
   for result in bing_web_search_results["webPages"]["value"]:
      combined_results.append(str(result['snippet']))

   # Flatten the list into a single string
   combined_results = '\n\n'.join(combined_results)

   # Generate additional from OpenAI GPT's model if possible
   additional_generated_data = generate_additional_data(query=query, model=model)

   # Append the additional data
   combined_results = additional_generated_data + '\n\n' + combined_results

   return combined_results


def bing_web_search(query: str, num_results: int, exact: bool = True) -> dict:
   """Perform a web search using Bing Web Search API
    
   Parameters:
      query (str): The search query.
      num_results (int): Number of search results to return.
      exact (bool): Whether to perform an exact search. Defaults to True.
   
   Returns:
      dict: The search results returned by Bing Web Search API.
   """
   subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
   endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/v7.0/search"

   # Exact expression search
   query = f'"{query}"' if exact else query

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


def bing_entity_search(query: str, exact: bool = True) -> dict:
   """Use Bing Entity Search API to get more relevant query information
    
   Parameters:
      query (str): The search query.
      exact (bool): Whether to perform an exact search. Defaults to True.
   
   Returns:
      dict: The search results returned by Bing Entity Search API.
   """
   subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
   endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/v7.0/entities"

   # Exact expression search
   query = f'"{query}"' if exact else query

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


def generate_additional_data(query: str, model: str = "gpt-3.5-turbo") -> str:
   """Generate additional data about the query using OpenAI GPT model.

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

